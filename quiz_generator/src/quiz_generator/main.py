#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start
from quiz_generator.crews.template_generator_crew.template_generator_crew import TemplateGeneratorCrew


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


def kickoff():
    poem_flow = QuizGeneratorFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = QuizGeneratorFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
