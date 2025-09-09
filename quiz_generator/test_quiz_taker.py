#!/usr/bin/env python3
"""
Test script for QuizTakerCrew to verify it works correctly
"""

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from quiz_generator.crews.quiz_taker_crew.quiz_taker_crew import QuizTakerCrew

def test_quiz_taker():
    """Test the QuizTakerCrew with an existing quiz"""
    
    print("🧪 Testing QuizTakerCrew...")
    
    # Use an existing quiz file
    quiz_file = "outputs/AI_102_speech_service_quiz.md"
    output_file = "outputs/AI_102_speech_service_completed_quiz.md"
    
    # Check if quiz file exists
    if not os.path.exists(quiz_file):
        print(f"❌ Quiz file not found: {quiz_file}")
        return False
    
    try:
        # Initialize QuizTakerCrew
        quiz_taker_crew = QuizTakerCrew(
            provider="azure",
            certification="AI_102", 
            quiz_file=quiz_file
        )
        
        # Set output file for the task
        quiz_taking_task = quiz_taker_crew.quiz_taking_task()
        quiz_taking_task.output_file = output_file
        
        print(f"📖 Reading quiz from: {quiz_file}")
        print(f"📝 Will save completed quiz to: {output_file}")
        
        # Run the crew
        result = quiz_taker_crew.crew().kickoff(inputs={
            "topic": "Speech Service", 
            "certification": "AI_102"
        })
        
        print("✅ QuizTakerCrew completed successfully!")
        print(f"📄 Completed quiz saved to: {output_file}")
        
        # Check if output file was created
        if os.path.exists(output_file):
            print("✅ Output file created successfully!")
            
            # Show a preview of the completed quiz
            with open(output_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print("\n📋 Preview of completed quiz (first 500 chars):")
                print("-" * 50)
                print(content[:500] + "..." if len(content) > 500 else content)
                print("-" * 50)
            
            return True
        else:
            print("❌ Output file was not created!")
            return False
            
    except Exception as e:
        print(f"❌ Error during quiz taking: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_quiz_taker()
    if success:
        print("\n🎉 Test completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Test failed!")
        sys.exit(1)
