"""
Template generation crew for drafting the quiz scaffold.

This module defines a crew that creates a Markdown template used to structure
the quiz. Agents and tasks are configured via YAML.

Classes
-------
TemplateGeneratorCrew
    Crew that outputs `outputs/quiz_template.md`.

Examples
--------
>>> from quiz_generator.crews.template_generator_crew.template_generator_crew import TemplateGeneratorCrew
>>> crew = TemplateGeneratorCrew()
>>> result = crew.crew().kickoff()
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class TemplateGeneratorCrew():
    """Crew that generates the initial quiz template in Markdown.

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
    def template_generator(self) -> Agent:
        """Build the template generator agent.

        Returns:
            Agent: Configured agent that drafts the quiz template.
        """
        return Agent(
            config=self.agents_config['template_generator'],
            verbose=True,
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task  
    @task
    def template_generator_task(self) -> Task:
        """Create the task that outputs the quiz template Markdown file.

        Returns:
            Task: Task definition producing `outputs/quiz_template.md`.
        """
        return Task(
            config=self.tasks_config['template_generator_task'],
            output_file='outputs/quiz_template.md'
        )

    @crew
    def crew(self) -> Crew:
        """Create the `Crew` instance for template generation.

        Returns:
            Crew: Sequential process wiring the template agent to its task.
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