#!/usr/bin/env python3
"""
Simple test script for Quick Quiz Generator testing.
This script directly calls the QuizGeneratorFlow with predefined state.
"""

import os
import sys

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.quiz_generator.main import QuizGeneratorFlow, QuizGeneratorState


def test_with_direct_state():
    """
    Test by directly setting the state instead of mocking user input.
    """
    print("🧪 Direct State Test - Quiz Generator Flow")
    print("=" * 60)
    
    try:
        # Create the flow
        quiz_flow = QuizGeneratorFlow()
        
        # Manually set the state with our test values
        quiz_flow.state.provider = "azure"
        quiz_flow.state.certification = "AI_900"
        quiz_flow.state.topic = "azure-ai-services-luis"  # One of the available topics
        quiz_flow.state.number_of_questions = 7
        quiz_flow.state.question_type = "mixed"
        
        print("📋 Test Configuration:")
        print(f"   - Provider: {quiz_flow.state.provider}")
        print(f"   - Certification: {quiz_flow.state.certification}")
        print(f"   - Topic: {quiz_flow.state.topic}")
        print(f"   - Questions: {quiz_flow.state.number_of_questions}")
        print(f"   - Type: {quiz_flow.state.question_type}")
        print("=" * 60)
        
        # Skip user input and start from database initialization
        print("\n🔧 Starting from database initialization...")
        
        # Step 1: Initialize database
        quiz_flow.initialize_vector_database()
        if quiz_flow.state.error_message:
            print(f"❌ Database initialization failed: {quiz_flow.state.error_message}")
            return False
        
        # Step 2: Generate template
        quiz_flow.generate_quiz_template()
        if quiz_flow.state.error_message:
            print(f"❌ Template generation failed: {quiz_flow.state.error_message}")
            return False
        
        # Step 3: Generate quiz with RAG
        quiz_flow.generate_quiz_with_rag_crew()
        if quiz_flow.state.error_message:
            print(f"❌ RAG crew failed: {quiz_flow.state.error_message}")
            return False
        
        # Step 4: Create final quiz
        quiz_flow.create_final_quiz()
        if quiz_flow.state.error_message:
            print(f"❌ Quiz maker failed: {quiz_flow.state.error_message}")
            return False
        
        # Step 5: Take quiz (student simulation)
        quiz_flow.take_quiz()
        if quiz_flow.state.error_message:
            print(f"❌ Quiz taker failed: {quiz_flow.state.error_message}")
            return False
        
        # Step 6: Evaluate quiz
        quiz_flow.evaluate_quiz()
        if quiz_flow.state.error_message:
            print(f"❌ Quiz evaluation failed: {quiz_flow.state.error_message}")
            return False
        
        # Step 7: Finalize
        quiz_flow.finalize_flow()
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def check_available_topics():
    """
    Check what topics are available in the dataset.
    """
    print("📂 Checking available topics...")
    
    dataset_path = os.path.join("src", "quiz_generator", "dataset", "azure", "AI_900")
    
    if os.path.exists(dataset_path):
        files = [f[:-4] for f in os.listdir(dataset_path) if f.endswith('.pdf')]
        print(f"📄 Found {len(files)} topics:")
        for i, topic in enumerate(files, 1):
            print(f"   {i}. {topic}")
        return files
    else:
        print(f"❌ Dataset path not found: {dataset_path}")
        return []


def main():
    """
    Main test function.
    """
    print("🚀 Quick Quiz Generator Test")
    print("Testing with: azure/AI_900, 7 questions, mixed type\n")
    
    # Check available topics first
    topics = check_available_topics()
    if not topics:
        print("❌ No topics found. Cannot proceed with test.")
        return 1
    
    print(f"\n🎯 Using topic: {topics[0]}")
    
    # Run the test
    success = test_with_direct_state()
    
    if success:
        print("\n🎉 Test completed successfully!")
        
        # Show generated files
        output_dir = "outputs"
        if os.path.exists(output_dir):
            files = [f for f in os.listdir(output_dir) if os.path.isfile(os.path.join(output_dir, f))]
            print(f"\n📁 Generated {len(files)} files:")
            for file in sorted(files):
                file_path = os.path.join(output_dir, file)
                size = os.path.getsize(file_path)
                print(f"   📄 {file} ({size} bytes)")
        
        return 0
    else:
        print("\n❌ Test failed!")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
