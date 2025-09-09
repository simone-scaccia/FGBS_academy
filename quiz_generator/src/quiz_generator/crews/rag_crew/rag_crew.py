"""
RAG (Retrieval-Augmented Generation) crew for certification quiz research.

This module implements a specialized crew that performs retrieval-augmented
research over a curated knowledge base and compiles structured outputs for
quiz generation workflows. It wires a research agent with a reporting agent
and tasks configured via YAML.

Classes
-------
RagCrew
    Crew that orchestrates RAG queries and reporting for quiz content.

Examples
--------
>>> from quiz_generator.crews.rag_crew.rag_crew import RagCrew
>>> crew = RagCrew(provider="azure", certification="ai900")
>>> result = crew.crew().kickoff(inputs={"topic": "Fundamentals of AI"})
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from quiz_generator.tools.rag_qdrant_tool import RagTool
from crewai_tools import FileReadTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class RagCrew():
    """Crew that performs research via Retrieval-Augmented Generation (RAG).

    Attributes:
        agents (List[BaseAgent]): Agents created from YAML configuration.
        tasks (List[Task]): Tasks created from YAML configuration.
        provider (str | None): Provider name used to scope collection search.
        certification (str | None): Certification name used to scope search.
    """

    agents: List[BaseAgent]
    tasks: List[Task]
    
    # Provider and certification for RAG tool configuration
    provider: str = None
    certification: str = None

    def __init__(self, provider: str = None, certification: str = None, **kwargs):
        """Initialize crew with collection-scoped RAG options.

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
    def researcher(self) -> Agent:
        """Build the research agent that queries the RAG index.

        Returns:
            Agent: Configured agent for retrieving and synthesizing knowledge.
        """
        return Agent(
            config=self.agents_config['researcher'], # type: ignore[index]
            tools=[RagTool(provider=self.provider, certification=self.certification)],
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        """Build the reporting agent that compiles results.

        Returns:
            Agent: Configured agent that structures findings and reads templates.
        """
        return Agent(
            config=self.agents_config['reporting_analyst'], # type: ignore[index]
            tools=[RagTool(provider=self.provider, certification=self.certification),
                   FileReadTool(file_path='outputs/quiz_template.md')],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
        """Create the task that performs the research phase.

        Returns:
            Task: Task definition for gathering sources and notes.
        """
        return Task(
            config=self.tasks_config['research_task'], # type: ignore[index]
        )

    @task
    def reporting_task(self) -> Task:
        """Create the task that compiles the research into structured output.

        Returns:
            Task: Task definition producing `outputs/questions.json`.
        """
        return Task(
            config=self.tasks_config['reporting_task'], # type: ignore[index]
            output_file='outputs/questions.json'
        )

    @crew
    def crew(self) -> Crew:
        """Create the `Crew` instance for RAG research and reporting.

        Returns:
            Crew: Sequential process wiring the research and reporting agents.
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
