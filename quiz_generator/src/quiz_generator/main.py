#!/usr/bin/env python
"""
Main module for Quiz Generator application.
This module handles user interaction and initializes the Qdrant database.
"""

import os
import sys
from quiz_generator.crews.database_crew.database_crew import DatabaseCrew

from random import randint
 
from pydantic import BaseModel
 
from crewai.flow import Flow, listen, start

from quiz_generator.crews.template_generator_crew.template_generator_crew import TemplateGeneratorCrew
from quiz_generator.crews.quiz_maker_crew.quiz_maker_crew import QuizMakerCrew


class QuizGeneratorState(BaseModel):
    question_count: int = None
    question_type: str = None


class QuizGeneratorFlow(Flow[QuizGeneratorState]):

    @start()
    def user_inputs(self):
        if self.state.question_count is None:
            # Question: choose the number of questions
            question_count = int(input("How many questions do you want in the quiz? (1-5) "))
            if question_count < 1 or question_count > 5:
                print("Invalid number of questions. Please choose between 1 and 5.")
                return self.user_inputs()
            else:
                self.state.question_count = question_count
        if self.state.question_type is None:
            # Question: choose between open answer, multiple choice, true/false, mixed
            question_type = input("What type of questions do you want? (open, multiple, true/false, mixed) ").strip().lower()
            if question_type not in ["open", "multiple", "true/false", "mixed"]:
                print("Invalid question type. Please choose between open, multiple, true/false, mixed.")
                return self.user_inputs()
            else:
                self.state.question_type = question_type
        print(f"Generating a quiz with {self.state.question_count} questions of type {self.state.question_type}.")

    @listen(user_inputs)
    def generate_quiz_template(self):

        crew = TemplateGeneratorCrew().crew().kickoff(
            inputs={
                "question_count": self.state.question_count,
                "question_type": self.state.question_type,
            }
        )

        print("Quiz template generated and saved to outputs/quiz_template.md")

    @listen(generate_quiz_template)
    def generate_quiz(self):
        input_json = {
            "questions": [
                {
                "type": "multiple_choice",
                "question": "Which service is used for orchestrating ETL pipelines in Azure?",
                "options": [
                    "Azure Logic Apps",
                    "Azure Data Factory",
                    "Azure DevOps",
                    "Azure Blob Storage"
                ],
                "answer": "Azure Data Factory"
                },
                {
                "type": "multiple_choice",
                "question": "Which Azure service provides serverless compute?",
                "options": [
                    "Azure Kubernetes Service",
                    "Azure Functions",
                    "Azure Virtual Machines",
                    "Azure App Service (Dedicated)"
                ],
                "answer": "Azure Functions"
                },
                {
                "type": "true_false",
                "question": "Azure SQL Database automatically backs up your database.",
                "options": ["True", "False"],
                "answer": "True"
                },
                {
                "type": "open_ended",
                "question": "Explain how to secure an API using Azure API Management.",
                "answer": ""
                },
                {
                "type": "open_ended",
                "question": "Describe a scenario where using Azure Virtual Network (VNet) peering would be beneficial.",
                "answer": ""
                }
            ]
        }

        quiz_maker_crew = QuizMakerCrew().crew().kickoff(
            inputs={
                "questions": input_json
            }
        )

        print("Quiz generated and saved to outputs/quiz.md")


def kickoff():
    poem_flow = QuizGeneratorFlow()
    poem_flow.kickoff()
 
 
def plot():
    poem_flow = QuizGeneratorFlow()
    poem_flow.plot()
 
 
if __name__ == "__main__":
    kickoff()



    
def get_available_providers():
    """Get list of available providers from dataset folder."""
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset")
    providers = []
    
    if os.path.exists(dataset_path):
        providers = [d for d in os.listdir(dataset_path) 
                    if os.path.isdir(os.path.join(dataset_path, d))]
    
    return providers


def get_available_certifications(provider):
    """Get list of available certifications for a given provider."""
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset", provider)
    certifications = []
    
    if os.path.exists(dataset_path):
        certifications = [d for d in os.listdir(dataset_path) 
                         if os.path.isdir(os.path.join(dataset_path, d))]
    
    return certifications


def initialize_database(provider, certification):
    """
    Initialize Qdrant database using DatabaseCrew.
    
    Args:
        provider (str): The provider name
        certification (str): The certification name
        
    Returns:
        bool: True if initialization was successful, False otherwise
    """
    print(f"🚀 Initializing Qdrant database...")
    print(f"📋 Provider: {provider}")
    print(f"🎓 Certification: {certification}")
    
    try:
        # Initialize and run DatabaseCrew
        database_crew = DatabaseCrew()
        result = database_crew.crew().kickoff(inputs={
            "provider": provider,
            "certification": certification
        })
        
        print("✅ Database initialization completed successfully!")
        print(f"📊 Result: {result.raw}")
        return True
        
    except Exception as e:
        print(f"❌ Error during database initialization: {str(e)}")
        return False


def main():
    """Main function to handle user interaction and database initialization."""
    print("🎯 Welcome to Quiz Generator!")
    print("=" * 50)
    
    # Get available providers
    providers = get_available_providers()
    
    if not providers:
        print("❌ No providers found in dataset folder!")
        sys.exit(1)
    
    # Display available providers
    print("📁 Available providers:")
    for i, provider in enumerate(providers, 1):
        print(f"  {i}. {provider}")
    
    # Get provider input from user
    while True:
        try:
            provider_choice = input(f"\n🔗 Select a provider (1-{len(providers)}): ").strip()
            provider_index = int(provider_choice) - 1
            
            if 0 <= provider_index < len(providers):
                selected_provider = providers[provider_index]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(providers)}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n� Goodbye!")
            sys.exit(0)
    
    # Get available certifications for selected provider
    certifications = get_available_certifications(selected_provider)
    
    if not certifications:
        print(f"❌ No certifications found for provider '{selected_provider}'!")
        sys.exit(1)
    
    # Display available certifications
    print(f"\n🎓 Available certifications for '{selected_provider}':")
    for i, certification in enumerate(certifications, 1):
        print(f"  {i}. {certification}")
    
    # Get certification input from user
    while True:
        try:
            cert_choice = input(f"\n📚 Select a certification (1-{len(certifications)}): ").strip()
            cert_index = int(cert_choice) - 1
            
            if 0 <= cert_index < len(certifications):
                selected_certification = certifications[cert_index]
                break
            else:
                print(f"❌ Please enter a number between 1 and {len(certifications)}")
        except ValueError:
            print("❌ Please enter a valid number")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)
    
    # Initialize database with selected provider and certification
    print(f"\n🔧 You selected:")
    print(f"   Provider: {selected_provider}")
    print(f"   Certification: {selected_certification}")
    
    confirm = input("\n❓ Do you want to initialize the database? (y/N): ").strip().lower()
    
    if confirm in ['y', 'yes']:
        success = initialize_database(selected_provider, selected_certification)
        
        if success:
            print("\n🎉 Database initialization completed successfully!")
            print("🚀 You can now use the quiz generator with this database.")
        else:
            print("\n⚠️ Database initialization failed!")
            print("🔍 Please check the logs for more details.")
    else:
        print("👋 Database initialization cancelled.")


if __name__ == "__main__":
    main()
