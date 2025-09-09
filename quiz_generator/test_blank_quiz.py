#!/usr/bin/env python3
"""
Test script to verify blank quiz generation (without answers in open questions)
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from quiz_generator.crews.quiz_maker_crew.quiz_maker_crew import QuizMakerCrew

def test_blank_quiz_generation():
    """Test that QuizMakerCrew generates blank quiz without answers"""
    
    # Test data
    questions_json_path = "outputs/AI_102_document_intelligence_questions.json"
    template_path = "outputs/AI_102_document_intelligence_template.md"
    quiz_md_path = "outputs/test_blank_quiz.md"
    quiz_pdf_path = "outputs/test_blank_quiz.pdf"
    
    if not os.path.exists(questions_json_path):
        print(f"❌ Questions JSON not found: {questions_json_path}")
        return False
        
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return False
    
    print("🧪 Testing blank quiz generation...")
    
    try:
        # Initialize QuizMaker crew
        quiz_maker_crew = QuizMakerCrew()
        
        # Run the crew
        result = quiz_maker_crew.crew().kickoff(inputs={
            'questions_json_path': questions_json_path,
            'template_path': template_path,
            'quiz_md_filename': quiz_md_path,
            'quiz_pdf_filename': quiz_pdf_path,
            'number_of_questions': 7
        })
        
        print(f"✅ QuizMaker crew completed")
        print(f"📝 Result: {result}")
        
        # Check if the file was created
        if os.path.exists(quiz_md_path):
            print(f"✅ Quiz file created: {quiz_md_path}")
            
            # Read and check content
            with open(quiz_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for answers in open questions (should NOT be present)
            lines = content.split('\n')
            in_open_question = False
            has_unwanted_answers = False
            
            for i, line in enumerate(lines):
                if "Short Open Questions" in line or "Open Questions" in line:
                    in_open_question = True
                    print("📝 Found open questions section")
                    continue
                    
                if in_open_question and line.strip().startswith("__") and not line.strip() == "__________________________________________________________":
                    # Found a line that starts with __ but contains text (answer)
                    print(f"❌ Found answer in open question: {line.strip()}")
                    has_unwanted_answers = True
            
            if not has_unwanted_answers:
                print("✅ No unwanted answers found in open questions")
                return True
            else:
                print("❌ Found unwanted answers in open questions")
                return False
        else:
            print(f"❌ Quiz file not created: {quiz_md_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_blank_quiz_generation()
    if success:
        print("\n🎉 Test PASSED - Blank quiz generated correctly!")
    else:
        print("\n💥 Test FAILED - Issues with blank quiz generation")
    
    sys.exit(0 if success else 1)
