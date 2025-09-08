from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from quiz_generator.src.quiz_generator.tools.db_tools import load_pdf

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class DatabaseCrew():
    """DatabaseCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def PDF_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['PDF_formatter'], # type: ignore[index]
            verbose=True,
            tools=[load_pdf()]
        )

    @agent
    def DB_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config['DB_engineer'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def load_and_structure_pdfs_task(self) -> Task:
        return Task(
            config=self.tasks_config['load_and_structure_pdfs_task'], # type: ignore[index]
        )

    @task
    def create_qdrant_db_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_qdrant_db_task'], # type: ignore[index]
        )

    @task
    def load_documents_to_qdrant_task(self) -> Task:
        return Task(
            config=self.tasks_config['load_documents_to_qdrant_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DatabaseCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
