"""
Test file for Azure AI-900 quiz generation.
"""

import os
import sys
from pathlib import Path

# Add src to the path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

# Import the Flow class
from quiz_generator.main import QuizGeneratorFlow

def test_quiz_generation_azure_ai900():
    """Test quiz generation for Azure AI-900 certification."""
    
    # Configuration parameters
    provider = "azure"
    certification = "AI_900"
    topic = "1"  # LUIS topic
    number_of_questions = 7
    question_type = "Mixed"
    
    print(f"🧪 Starting test with parameters:")
    print(f"   Provider: {provider}")
    print(f"   Certification: {certification}")
    print(f"   Topic: {topic}")
    print(f"   Number of questions: {number_of_questions}")
    print(f"   Question type: {question_type}")
    
    # Create Flow instance
    flow = QuizGeneratorFlow()
    
    # Create user input dict to simulate user selections
    user_input = {
        'provider': provider,
        'certification': certification,
        'topic': topic,
        'number_of_questions': number_of_questions,
        'question_type': question_type
    }
    
    # Execute the flow
    try:
        result = flow.kickoff(inputs=user_input)
        print(f"✅ Test completed successfully!")
        print(f"Result: {result}")
        return True
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        raise e

if __name__ == "__main__":
    test_quiz_generation_azure_ai900()
