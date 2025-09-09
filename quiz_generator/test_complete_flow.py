#!/usr/bin/env python3
"""
Test script for the complete Quiz Generator Flow.
This script automatically tests the entire workflow with predefined inputs.
"""

import os
import sys
from unittest.mock import patch
from io import StringIO

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.quiz_generator.main import QuizGeneratorFlow


def mock_user_input_sequence():
    """
    Mock user input sequence for automated testing.
    
    Simulates user selections:
    - Provider: azure (choice 1)
    - Certification: AI_900 (choice 1) 
    - Topic: first available topic (choice 1)
    - Number of questions: 7
    - Question type: mixed (choice 4)
    """
    inputs = iter([
        "1",    # Provider selection: azure
        "1",    # Certification selection: AI_900
        "1",    # Topic selection: first available topic
        "7",    # Number of questions
        "4"     # Question type: mixed (assuming it's option 4)
    ])
    return lambda prompt="": next(inputs)


def test_complete_workflow():
    """
    Test the complete Quiz Generator workflow with predefined inputs.
    """
    print("🧪 Starting Complete Quiz Generator Flow Test")
    print("=" * 60)
    print("📋 Test Configuration:")
    print("   - Provider: azure")
    print("   - Certification: AI_900")
    print("   - Topic: First available topic")
    print("   - Questions: 7")
    print("   - Type: mixed")
    print("=" * 60)
    
    # Mock the input function to provide automated responses
    with patch('builtins.input', side_effect=mock_user_input_sequence()):
        try:
            # Initialize and run the Quiz Generator Flow
            quiz_flow = QuizGeneratorFlow()
            quiz_flow.kickoff()
            
            print("\n" + "=" * 60)
            print("🎉 TEST COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            
            # Check if output files were created
            output_files = [
                "outputs/quiz_template.md",
                "outputs/questions.json", 
                "outputs/quiz.md",
                "outputs/quiz.pdf",
                "outputs/completed_quiz.md",
                "outputs/quiz_evaluation.md"
            ]
            
            print("📄 Checking generated files:")
            for file_path in output_files:
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    print(f"   ✅ {file_path} ({file_size} bytes)")
                else:
                    print(f"   ❌ {file_path} (not found)")
            
            return True
            
        except Exception as e:
            print(f"\n❌ TEST FAILED: {str(e)}")
            import traceback
            traceback.print_exc()
            return False


def test_individual_components():
    """
    Test individual components with mock data.
    """
    print("\n🔧 Testing Individual Components")
    print("-" * 40)
    
    # Test imports
    try:
        from src.quiz_generator.crews.rag_crew.rag_crew import RagCrew
        from src.quiz_generator.crews.template_generator_crew.template_generator_crew import TemplateGeneratorCrew  
        from src.quiz_generator.crews.quiz_maker_crew.quiz_maker_crew import QuizMakerCrew
        from src.quiz_generator.crews.quiz_taker_crew.quiz_taker_crew import QuizTakerCrew
        from src.quiz_generator.crews.quiz_evaluator_crew.quiz_evaluator_crew import QuizEvaluatorCrew
        print("✅ All crew imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test crew initialization
    try:
        rag_crew = RagCrew(provider="azure", certification="AI_900")
        template_crew = TemplateGeneratorCrew()
        quiz_maker_crew = QuizMakerCrew()
        quiz_taker_crew = QuizTakerCrew(provider="azure", certification="AI_900")
        quiz_evaluator_crew = QuizEvaluatorCrew()
        print("✅ All crew initialization successful")
    except Exception as e:
        print(f"❌ Crew initialization error: {e}")
        return False
    
    return True


def display_test_results():
    """
    Display the results of the test run.
    """
    print("\n📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    output_dir = "outputs"
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        if files:
            print(f"📁 Generated {len(files)} output files:")
            for file in sorted(files):
                file_path = os.path.join(output_dir, file)
                if os.path.isfile(file_path):
                    size = os.path.getsize(file_path)
                    print(f"   📄 {file} ({size} bytes)")
        else:
            print("❌ No output files generated")
    else:
        print("❌ Output directory not found")


def main():
    """
    Main test function.
    """
    print("🚀 Quiz Generator Complete Flow Test")
    print("This test will automatically run the entire quiz generation workflow")
    print("with predefined inputs to verify everything works correctly.\n")
    
    # Test individual components first
    if not test_individual_components():
        print("❌ Component tests failed. Aborting workflow test.")
        return 1
    
    # Run the complete workflow test
    success = test_complete_workflow()
    
    # Display results
    display_test_results()
    
    if success:
        print("\n🎉 All tests passed! The Quiz Generator is working correctly.")
        return 0
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
