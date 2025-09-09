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
from .crews.quiz_taker_crew.quiz_taker_crew import QuizTakerCrew
from .crews.quiz_evaluator_crew.quiz_evaluator_crew import QuizEvaluatorCrew
from .utils.user_utils import get_user_selections, get_user_choices, display_selection_summary
from .utils.database_utils import initialize_database

class QuizGeneratorState(BaseModel):
    """State model for the Quiz Generator Flow."""
    provider: Optional[str] = None
    certification: Optional[str] = None
    topic: Optional[str] = None
    number_of_questions: int = None
    question_type: str = None
    database_initialized: bool = False
    quiz_generated: bool = False
    quiz_completed: bool = False
    quiz_evaluated: bool = False
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
            
            # Step 2: Collect info about quiz template to generate
            # Get user choices
            number_of_questions, question_type = get_user_choices()
            
            if not all([number_of_questions, question_type]):
                self.state.error_message = "User cancelled or invalid quiz configuration"
                return
            
            # Update state with quiz configuration
            self.state.number_of_questions = number_of_questions
            self.state.question_type = question_type
            
            # Display selection summary
            display_selection_summary(provider, certification, topic, number_of_questions, question_type)
            print("✅ User input selection collected successfully!")
            print(f"This system will generate {number_of_questions} questions of type '{question_type}' for the certification {certification}, focusing on these topics: {topic}")
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
    def generate_quiz_template(self):
        """
        Step 2.5: Generate quiz template using the Template Generator crew.
        """
        if self.state.error_message:
            print("⏭️ Skipping quiz template generation due to previous error")
            return
        
        print(f"\n� Generating quiz template for {self.state.provider}/{self.state.certification}... with choices done")
        
        try:
            # Initialize and run Template Generator crew with provider/certification configuration
            template_crew = TemplateGeneratorCrew()
            template_result = template_crew.crew().kickoff(inputs={
                "provider": self.state.provider.capitalize(),
                "certification": self.state.certification,
                "number_of_questions": self.state.number_of_questions,
                "question_type": self.state.question_type
            })
            
            print("✅ Quiz template generated successfully!")
            print(f"📝 Generated Template:\n{template_result}")
            
        except Exception as e:
            self.state.error_message = f"Error during quiz template generation: {str(e)}"
            print(f"❌ {self.state.error_message}")

    @listen(generate_quiz_template)
    def generate_quiz_with_rag_crew(self):
        """
        Step 4: Generate quiz questions using the RAG crew with the initialized database.
        """
        if self.state.error_message or not self.state.database_initialized:
            print("⏭️ Skipping quiz generation due to previous error or failed database initialization")
            return
        
        print(f"\n📝 Starting RAG crew for topic: {self.state.topic}")
        
        try:
            current_year = datetime.now().year
            
            # Initialize and run RAG crew with provider/certification configuration
            rag_crew = RagCrew(provider=self.state.provider, certification=self.state.certification)
            rag_crew.crew().kickoff(inputs={
                "topic": self.state.topic,
                "current_year": current_year,
                "number_of_questions": self.state.number_of_questions,
                "question_type": self.state.question_type
            })
            
            print("✅ RAG crew completed successfully!")
            print("📊 Quiz questions generated in JSON format!")
            
        except Exception as e:
            self.state.error_message = f"Error during quiz generation: {str(e)}"
            print(f"❌ {self.state.error_message}")

    @listen(generate_quiz_with_rag_crew)
    def create_final_quiz(self):
        """
        Step 5: Create final quiz using Quiz Maker crew to combine template and questions.
        """
        if self.state.error_message:
            print("⏭️ Skipping final quiz creation due to previous error")
            return
        
        print(f"\n📋 Creating final quiz with Quiz Maker crew...")
        
        try:
            # Initialize and run Quiz Maker crew
            quiz_maker_crew = QuizMakerCrew()
            quiz_result = quiz_maker_crew.crew().kickoff(inputs={
                "number_of_questions": self.state.number_of_questions
            })
            self.state.quiz_generated = True
            
            print("✅ Quiz Maker crew completed successfully!")
            print(f"📊 Final quiz generated successfully!")

        except Exception as e:
            self.state.error_message = f"Error during final quiz creation: {str(e)}"
            print(f"❌ {self.state.error_message}")

    '''@listen(create_final_quiz)
    def take_quiz(self):
        """
        Step 6: Simulate a student taking the quiz using Quiz Taker crew.
        """
        if self.state.error_message or not self.state.quiz_generated:
            print("⏭️ Skipping quiz taking due to previous error or quiz not generated")
            return
        
        print(f"\n🎓 Simulating student taking the quiz...")
        
        try:
            # Initialize and run Quiz Taker crew
            quiz_taker_crew = QuizTakerCrew(provider=self.state.provider, certification=self.state.certification)
            quiz_taker_result = quiz_taker_crew.crew().kickoff(inputs={
                "topic": self.state.topic,
                "certification": self.state.certification
            })
            self.state.quiz_completed = True
            
            print("✅ Quiz Taker crew completed successfully!")
            print(f"📝 Student has completed the quiz!")
            print(f"💾 Completed quiz saved to: outputs/completed_quiz.md")

        except Exception as e:
            self.state.error_message = f"Error during quiz taking: {str(e)}"
            print(f"❌ {self.state.error_message}")

    @listen(take_quiz)
    def evaluate_quiz(self):
        """
        Step 7: Evaluate the completed quiz using Quiz Evaluator crew.
        """
        if self.state.error_message or not self.state.quiz_completed:
            print("⏭️ Skipping quiz evaluation due to previous error or quiz not completed")
            return
        
        print(f"\n📊 Evaluating the completed quiz...")
        
        try:
            # Initialize and run Quiz Evaluator crew
            quiz_evaluator_crew = QuizEvaluatorCrew()
            quiz_evaluation_result = quiz_evaluator_crew.crew().kickoff(inputs={
                "topic": self.state.topic
            })
            self.state.quiz_evaluated = True
            
            print("✅ Quiz Evaluator crew completed successfully!")
            print(f"📈 Quiz evaluation completed!")
            print(f"💾 Evaluation report saved to: outputs/quiz_evaluation.md")

        except Exception as e:
            self.state.error_message = f"Error during quiz evaluation: {str(e)}"
            print(f"❌ {self.state.error_message}")'''

    @listen(create_final_quiz)
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
            print(f"❓ Number of Questions: {self.state.number_of_questions}")
            print(f"📝 Question Type: {self.state.question_type}")
            print("✅ Database initialized: Yes")
            print("✅ Quiz generated: Yes")
            #print(f"✅ Quiz completed by student: {self.state.quiz_completed}")
            #print(f"✅ Quiz evaluated: {self.state.quiz_evaluated}")
            if self.state.quiz_evaluated:
                print("📄 Files generated:")
                print("   - outputs/quiz_template.md (template)")
                print("   - outputs/questions.json (questions data)")
                print("   - outputs/quiz.md (blank quiz)")
                print("   - outputs/quiz.pdf (blank quiz PDF)")
                #print("   - outputs/completed_quiz.md (completed quiz)")
                #print("   - outputs/quiz_evaluation.md (evaluation report)")
        else:
            print("⚠️ Flow completed with issues")
            print(f"✅ Database initialized: {self.state.database_initialized}")
            print(f"❌ Quiz generated: {self.state.quiz_generated}")
            #print(f"❌ Quiz completed: {self.state.quiz_completed}")
            #print(f"❌ Quiz evaluated: {self.state.quiz_evaluated}")


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
    plot()
    main()


if __name__ == "__main__":
    main()
