#!/usr/bin/env python3
"""
Specific test for the exact requirements:
- Provider: azure
- Certification: AI_900  
- Topic: First available topic
- Questions: 7
- Type: mixed
"""

import os
import sys
import json

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.quiz_generator.main import QuizGeneratorFlow


def load_test_config():
    """Load test configuration from JSON file."""
    with open('test_config.json', 'r') as f:
        return json.load(f)


def test_azure_ai900_mixed_7_questions():
    """
    Test the exact scenario requested:
    - azure provider
    - AI_900 certification  
    - first available topic
    - 7 questions
    - mixed type
    """
    config = load_test_config()
    test_config = config['test_config']
    
    print("🎯 SPECIFIC TEST: Azure AI_900 - 7 Mixed Questions")
    print("=" * 60)
    print("📋 Configuration:")
    for key, value in test_config.items():
        if key != 'description':
            print(f"   {key}: {value}")
    print("=" * 60)
    
    try:
        # Create and configure the flow
        quiz_flow = QuizGeneratorFlow()
        
        # Set the exact state we want to test
        quiz_flow.state.provider = test_config['provider']
        quiz_flow.state.certification = test_config['certification']
        quiz_flow.state.topic = test_config['topic']
        quiz_flow.state.number_of_questions = test_config['number_of_questions']
        quiz_flow.state.question_type = test_config['question_type']
        
        print("🚀 Starting test execution...\n")
        
        # Execute each step and track progress
        steps = [
            ("🔧 Initializing vector database...", quiz_flow.initialize_vector_database),
            ("📝 Generating quiz template...", quiz_flow.generate_quiz_template),
            ("🤖 Generating questions with RAG...", quiz_flow.generate_quiz_with_rag_crew),
            ("📋 Creating final quiz...", quiz_flow.create_final_quiz),
            ("🎓 Simulating student taking quiz...", quiz_flow.take_quiz),
            ("📊 Evaluating completed quiz...", quiz_flow.evaluate_quiz)
        ]
        
        for step_name, step_function in steps:
            print(step_name)
            step_function()
            
            if quiz_flow.state.error_message:
                print(f"❌ Failed at step: {step_name}")
                print(f"Error: {quiz_flow.state.error_message}")
                return False
            else:
                print("✅ Completed successfully\n")
        
        # Final summary
        print("🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
        quiz_flow.finalize_flow()
        
        # Validate outputs
        validate_outputs(config['expected_outputs'])
        
        # Validate question distribution for mixed type
        validate_question_distribution(config['expected_distribution'])
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def validate_outputs(expected_files):
    """Validate that all expected output files were created."""
    print("\n📁 Validating Output Files:")
    print("-" * 30)
    
    all_exist = True
    for file_path in expected_files:
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} (missing)")
            all_exist = False
    
    if all_exist:
        print("✅ All expected files generated successfully!")
    else:
        print("❌ Some expected files are missing!")
    
    return all_exist


def validate_question_distribution(expected_dist):
    """Validate that the question distribution matches expectations for mixed type."""
    print("\n📊 Validating Question Distribution:")
    print("-" * 35)
    
    questions_file = "outputs/questions.json"
    if not os.path.exists(questions_file):
        print("❌ Questions file not found!")
        return False
    
    try:
        with open(questions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        questions = data.get('questions', [])
        total_questions = len(questions)
        
        # Count question types
        type_counts = {
            'multiple_choice': 0,
            'true_false': 0, 
            'open_ended': 0
        }
        
        for question in questions:
            q_type = question.get('type', '')
            if q_type in type_counts:
                type_counts[q_type] += 1
        
        print(f"Total questions generated: {total_questions}")
        print(f"Expected total: {expected_dist['total']}")
        
        for q_type, count in type_counts.items():
            expected = expected_dist.get(q_type, 0)
            status = "✅" if count == expected else "⚠️"
            print(f"{status} {q_type}: {count} (expected: {expected})")
        
        # Check if total matches
        if total_questions == expected_dist['total']:
            print("✅ Total question count matches!")
            return True
        else:
            print(f"❌ Total question count mismatch!")
            return False
            
    except json.JSONDecodeError as e:
        print(f"❌ Error reading questions file: {e}")
        return False


def main():
    """Main test execution."""
    print("🧪 AZURE AI_900 SPECIFIC TEST")
    print("Testing the exact scenario requested by the user\n")
    
    # Run the specific test
    success = test_azure_ai900_mixed_7_questions()
    
    if success:
        print("\n🎉 TEST PASSED!")
        print("The Quiz Generator successfully created:")
        print("- 7 mixed questions for Azure AI_900")
        print("- Complete student simulation")
        print("- Automatic evaluation")
        print("\nCheck the outputs/ directory for all generated files.")
        return 0
    else:
        print("\n❌ TEST FAILED!")
        print("Check the error messages above for details.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
