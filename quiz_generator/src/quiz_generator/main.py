"""
Main module for Quiz Generator application.
This module implements the main Flow following CrewAI best practices.
"""

import os
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from .crews.rag_crew.rag_crew import RagCrew
from .crews.template_generator_crew.template_generator_crew import TemplateGeneratorCrew
from .crews.quiz_maker_crew.quiz_maker_crew import QuizMakerCrew

from .utils.user_utils import get_user_selections, get_user_choices, display_selection_summary
from .utils.database_utils import initialize_database, save_quiz_results

class QuizGeneratorState(BaseModel):
    """State model for the Quiz Generator Flow."""
    provider: Optional[str] = None
    certification: Optional[str] = None
    topic: Optional[str] = None
    number_of_questions: int = None
    question_type: int = None
    database_initialized: bool = False
    quiz_generated: bool = False
    output_filename: Optional[str] = None
    error_message: Optional[str] = None


class QuizGeneratorFlow(Flow[QuizGeneratorState]):
    """
    Main Flow for Quiz Generator following CrewAI best practices.
    
    This flow orchestrates the complete quiz generation process:
    1. User input collection
    2. Database initialization
    3. Quiz generation using RAG crew
    4. Results saving
    """

    @start()
    def collect_user_input(self):
        """
        Step 1: Collect user input for provider, certification, and topic selection.
        Step 2: Collect user choice about the number of questions and their type to generate for the practice quiz.
        """
        print("🚀 Starting Quiz Generator Flow...")
        
        # Get dataset path
        dataset_path = os.path.join(os.path.dirname(__file__), "dataset")
        
        try:

            # Step 1: Collect info about certification
            # Get user selections
            provider, certification, topic = get_user_selections(dataset_path)
            
            if not all([provider, certification, topic]):
                self.state.error_message = "User cancelled or invalid selection"
                return
            
            # Update state
            self.state.provider = provider
            self.state.certification = certification
            self.state.topic = topic
            
            # Display selection summary
            display_selection_summary(provider, certification, topic)
            print("✅ User input selection collected successfully!")
            
            # Step 2: Collect info about quiz template to generate
            # Get user choices
            number_of_questions, question_type = get_user_choices(dataset_path)
        except Exception as e:
            self.state.error_message = f"Error collecting user input: {str(e)}"
            print(f"❌ {self.state.error_message}")

    @listen(collect_user_input)
    def initialize_vector_database(self):
        """
        Step 3: Initialize the Qdrant vector database with documents from the selected certification.
        """
        if self.state.error_message:
            print("⏭️ Skipping database initialization due to previous error")
            return
        
        print(f"\n� Initializing database for {self.state.provider}/{self.state.certification}...")
        
        try:
            # Get dataset path
            dataset_path = os.path.join(os.path.dirname(__file__), "dataset")
            
            # Initialize database
            success = initialize_database(
                self.state.provider, 
                self.state.certification, 
                dataset_path
            )
            
            if success:
                self.state.database_initialized = True
                print("✅ Database initialization completed successfully!")
            else:
                self.state.error_message = "Database initialization failed"
                print("❌ Database initialization failed!")
                
        except Exception as e:
            self.state.error_message = f"Error during database initialization: {str(e)}"
            print(f"❌ {self.state.error_message}")

    @listen(initialize_vector_database)
    def generate_quiz_with_rag_crew(self):
        """
        Step 3: Generate quiz using the RAG crew with the initialized database.
        """
        if self.state.error_message or not self.state.database_initialized:
            print("⏭️ Skipping quiz generation due to previous error or failed database initialization")
            return
        
        print(f"\n� Starting RAG crew for topic: {self.state.topic}")
        
        try:
            current_year = datetime.now().year
            
            # Initialize and run RAG crew with provider/certification configuration
            rag_crew = RagCrew(provider=self.state.provider, certification=self.state.certification)
            crew_result = rag_crew.crew().kickoff(inputs={
                "topic": self.state.topic,
                "current_year": current_year
            })
            
            # Save results
            output_dir = os.path.join(os.path.dirname(__file__), "..", "..")
            output_filename = save_quiz_results(
                self.state.provider,
                self.state.certification,
                self.state.topic,
                crew_result,
                output_dir
            )
            
            self.state.quiz_generated = True
            self.state.output_filename = output_filename
            
            print("✅ RAG crew completed successfully!")
            print(f"📊 Quiz generated successfully!")
            print(f"💾 Results saved to: {output_filename}")
            
        except Exception as e:
            self.state.error_message = f"Error during quiz generation: {str(e)}"
            print(f"❌ {self.state.error_message}")

    @listen(generate_quiz_with_rag_crew)
    def finalize_flow(self):
        """
        Step 4: Finalize the flow and provide summary.
        """
        print("\n" + "=" * 60)
        print("📋 QUIZ GENERATOR FLOW SUMMARY")
        print("=" * 60)
        
        if self.state.error_message:
            print(f"❌ Flow completed with errors: {self.state.error_message}")
            return
        
        if self.state.quiz_generated:
            print("🎉 Flow completed successfully!")
            print(f"📁 Provider: {self.state.provider}")
            print(f"🎓 Certification: {self.state.certification}")
            print(f"🎯 Topic: {self.state.topic}")
            print(f"💾 Output file: {self.state.output_filename}")
            print("✅ Database initialized: Yes")
            print("✅ Quiz generated: Yes")
        else:
            print("⚠️ Flow completed with issues")
            print(f"✅ Database initialized: {self.state.database_initialized}")
            print(f"❌ Quiz generated: {self.state.quiz_generated}")


def main():
    """
    Main function to start the Quiz Generator Flow.
    
    This function follows CrewAI best practices by implementing the main logic
    as a Flow with proper state management and step-by-step execution.
    """
    try:
        # Initialize and run the Quiz Generator Flow
        quiz_flow = QuizGeneratorFlow()
        quiz_flow.kickoff()
        
    except KeyboardInterrupt:
        print("\n👋 Quiz Generator Flow interrupted by user")
    except Exception as e:
        print(f"\n❌ Quiz Generator Flow failed: {str(e)}")


def plot():
    """Plot the Quiz Generator Flow for visualization."""
    quiz_flow = QuizGeneratorFlow()
    quiz_flow.plot()


def kickoff():
    """Alternative entry point for the flow (CrewAI convention)."""
    main()


if __name__ == "__main__":
    main()
