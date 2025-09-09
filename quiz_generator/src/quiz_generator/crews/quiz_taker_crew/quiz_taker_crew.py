"""
Quiz taking crew that simulates a student answering the quiz.

This module defines a crew that reads the generated quiz and, when needed,
consults a RAG tool to look up knowledge scoped by provider/certification.
It outputs a completed quiz file ready for evaluation.

Classes
-------
QuizTakerCrew
    Crew that answers questions and writes `outputs/completed_quiz.md`.

Examples
--------
>>> from quiz_generator.crews.quiz_taker_crew.quiz_taker_crew import QuizTakerCrew
>>> crew = QuizTakerCrew(provider="azure", certification="ai900")
>>> result = crew.crew().kickoff()
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool
from typing import List

from quiz_generator.tools.rag_qdrant_tool import RagTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class QuizTakerCrew():
    """Crew that simulates a student taking the generated quiz.

    Attributes:
        agents (List[BaseAgent]): Agents created from YAML configuration.
        tasks (List[Task]): Tasks created from YAML configuration.
        provider (str | None): Provider name used to scope RAG searches.
        certification (str | None): Certification name used to scope RAG searches.
    """

    agents: List[BaseAgent]
    tasks: List[Task]
    
    # Provider and certification for RAG tool configuration
    provider: str = None
    certification: str = None

    def __init__(self, provider: str = None, certification: str = None, **kwargs):
        """Initialize crew with scoped Retrieval-Augmented Generation (RAG) options.

        Args:
            provider (str | None): Provider name for the RAG collection.
            certification (str | None): Certification name for the RAG collection.
            **kwargs: Additional keyword arguments forwarded to the base class.
        """
        super().__init__(**kwargs)
        self.provider = provider
        self.certification = certification

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def quiz_taker_student(self) -> Agent:
        """Build the quiz-taking agent configured for knowledge retrieval.

        The agent reads the produced quiz and can consult a RAG tool to search
        relevant knowledge based on the configured provider/certification.

        Returns:
            Agent: Configured agent that answers quiz questions.
        """
        return Agent(
            config=self.agents_config['quiz_taker_student'], # type: ignore[index]
            tools=[
                FileReadTool(file_path='outputs/quiz.md'), # Tool to read the generated quiz
                RagTool(provider=self.provider, certification=self.certification) # Tool to search knowledge base
            ],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def quiz_taking_task(self) -> Task:
        """Create the task that records the student's answers.

        Returns:
            Task: Task definition producing `outputs/completed_quiz.md`.
        """
        return Task(
            config=self.tasks_config['quiz_taking_task'], # type: ignore[index]
            output_file='outputs/completed_quiz.md'
        )

    @crew
    def crew(self) -> Crew:
        """Create the `Crew` instance for quiz taking.

        Returns:
            Crew: Sequential process wiring the student agent to its task.
        """
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
