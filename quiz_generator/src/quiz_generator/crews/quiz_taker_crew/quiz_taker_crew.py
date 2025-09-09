from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool
from typing import List
from quiz_generator.tools.md_to_pdf_tool import MarkdownToPdfExporter
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class QuizTakerCrew():
    """QuizTakerCrew crew - Simulates a student taking the quiz"""

    agents: List[BaseAgent]
    tasks: List[Task]
    
    # Provider and certification for RAG tool configuration
    provider: str = None
    certification: str = None
    quiz_file: str = None

    def __init__(self, provider: str = None, certification: str = None, quiz_file: str = None, **kwargs):
        """
        Initialize QuizTakerCrew with provider/certification for knowledge search.
        
        Args:
            provider (str, optional): Provider name for RAG collection
            certification (str, optional): Certification name for RAG collection
            quiz_file (str, optional): Path to the quiz file to complete
        """
        super().__init__(**kwargs)
        self.provider = provider
        self.certification = certification
        self.quiz_file = quiz_file or 'outputs/quiz.md'

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def quiz_taker_student(self) -> Agent:
        return Agent(
            config=self.agents_config['quiz_taker_student'], # type: ignore[index]
            tools=[
                FileReadTool(file_path=self.quiz_file), # Tool to read the generated quiz
                MarkdownToPdfExporter() # Tool to convert markdown to PDF 
            ],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def quiz_taking_task(self) -> Task:
        return Task(
            config=self.tasks_config['quiz_taking_task'] # type: ignore[index]
            # Note: output_file will be set dynamically
        )
    
    @task
    def completed_quiz_pdf_task(self) -> Task:
        return Task(
            config=self.tasks_config['completed_quiz_pdf_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the QuizTakerCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
