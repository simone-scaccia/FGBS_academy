"""
Quiz evaluation crew for grading completed quizzes.

This module implements a crew that reads the completed quiz and the canonical
answers, then produces an evaluation report. Configuration is provided via
YAML for both agents and tasks.

Classes
-------
QuizEvaluatorCrew
    Crew that generates `outputs/quiz_evaluation.md` from inputs.

Examples
--------
>>> from quiz_generator.crews.quiz_evaluator_crew.quiz_evaluator_crew import QuizEvaluatorCrew
>>> crew = QuizEvaluatorCrew()
>>> result = crew.crew().kickoff()
"""

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import FileReadTool
from typing import List

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class QuizEvaluatorCrew():
    """Crew responsible for evaluating a completed quiz against correct answers.

    This crew wires a single evaluator agent with one task that reads the
    completed quiz and the canonical answers to generate an evaluation report.

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
    def quiz_evaluator(self) -> Agent:
        """Build the quiz evaluator agent.

        The agent is configured via YAML and equipped with tools to read the
        completed quiz and the ground-truth answers.

        Returns:
            Agent: Configured agent that evaluates quiz responses.
        """
        return Agent(
            config=self.agents_config['quiz_evaluator'], # type: ignore[index]
            tools=[
                FileReadTool(file_path='outputs/completed_quiz.md'), # Tool to read the completed quiz
                FileReadTool(file_path='outputs/questions.json'), # Tool to read the correct answers
            ],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def quiz_evaluation_task(self) -> Task:
        """Create the task that evaluates the completed quiz.

        Returns:
            Task: Task definition that produces an evaluation markdown report.
        """
        return Task(
            config=self.tasks_config['quiz_evaluation_task'], # type: ignore[index]
            output_file='outputs/quiz_evaluation.md'
        )

    @crew
    def crew(self) -> Crew:
        """Create the `Crew` instance for quiz evaluation.

        Returns:
            Crew: Sequential process wiring the evaluator agent to its task.
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
