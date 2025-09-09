"""
Quiz generation crew for composing and exporting quizzes.

This module defines a crew that assembles a quiz from a Markdown template and
pre-computed questions, and can export the final result to PDF via a tool.
Agents and tasks are configured through YAML files.

Classes
-------
QuizMakerCrew
    Crew that produces `outputs/quiz.md` and optionally a PDF export.

Examples
--------
>>> from quiz_generator.crews.quiz_maker_crew.quiz_maker_crew import QuizMakerCrew
>>> crew = QuizMakerCrew()
>>> result = crew.crew().kickoff()
"""

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
class QuizMakerCrew():
    """Crew that generates a quiz and exports it to Markdown/PDF.

    Attributes:
        agents (List[BaseAgent]): Agents created from YAML configuration.
        tasks (List[Task]): Tasks created from YAML configuration.
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def quiz_maker(self) -> Agent:
        """Build the quiz maker agent.

        The agent reads a quiz template and the curated questions and can
        optionally export output to PDF via a tool.

        Returns:
            Agent: Configured agent that assembles the quiz content.
        """
        return Agent(
            config=self.agents_config['quiz_maker'], # type: ignore[index]
            tools=[FileReadTool(file_path='outputs/quiz_template.md'), # Tool to read the quiz template
                   FileReadTool(file_path='outputs/questions.json'), # Tool to read the questions JSON
                   MarkdownToPdfExporter() # Tool to convert markdown to PDF
                  ],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def quiz_maker_task(self) -> Task:
        """Create the task that composes the quiz Markdown file.

        Returns:
            Task: Task definition producing `outputs/quiz.md`.
        """
        return Task(
            config=self.tasks_config['quiz_maker_task'], # type: ignore[index]
            output_file='outputs/quiz.md'
        )
    
    @task
    def pdf_export_task(self) -> Task:
        """Create the task that exports the quiz to PDF.

        Returns:
            Task: Task definition responsible for PDF export.
        """
        return Task(
            config=self.tasks_config['pdf_export_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Create the `Crew` instance for quiz generation and export.

        Returns:
            Crew: Sequential process wiring the maker agent to its tasks.
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