from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, task, crew, after_kickoff
from tools.math_tools import (
    AddNumbersTool,
    SubtractNumbersTool,
    MultiplyNumbersTool,
    DivideNumbersTool,
)


@CrewBase
class CalculatorCrew:
    """A crew that performs basic mathematical operations"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self):
        self.tools = [
            AddNumbersTool(),
            SubtractNumbersTool(),
            MultiplyNumbersTool(),
            DivideNumbersTool(),
        ]

    @after_kickoff
    def process_output(self, output):
        """Process the output after the crew finishes"""
        output.raw += "\nCalculations completed successfully."
        return output

    @agent
    def calculator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["calculator_agent"],  # type: ignore
            tools=self.tools,
            verbose=True,
        )

    @task
    def addition_task(self) -> Task:
        return Task(
            config=self.tasks_config["addition_task"],  # type: ignore
            agent=self.calculator_agent(),
        )

    @task
    def subtraction_task(self) -> Task:
        return Task(
            config=self.tasks_config["subtraction_task"],  # type: ignore
            agent=self.calculator_agent(),
        )

    @task
    def multiplication_task(self) -> Task:
        return Task(
            config=self.tasks_config["multiplication_task"],  # type: ignore
            agent=self.calculator_agent(),
        )

    @task
    def division_task(self) -> Task:
        return Task(
            config=self.tasks_config["division_task"],  # type: ignore
            agent=self.calculator_agent(),
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,  # type: ignore
            tasks=self.tasks,  # type: ignore
            process=Process.sequential,
            verbose=True,
        )
