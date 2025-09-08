#!/usr/bin/env python
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
