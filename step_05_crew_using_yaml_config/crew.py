from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import yaml
from pathlib import Path
from dotenv import load_dotenv
import os

# Load API key from environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set")


class ConfigLoader:
    @staticmethod
    def load_config(filename: str) -> dict:
        config_path = Path("config") / filename
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(config_path) as f:
            return yaml.safe_load(f)


@CrewBase
class LatestAiDevelopmentCrew:
    """Crew for analyzing and reporting on latest AI developments"""

    def __init__(self):
        # Load YAML configs
        self.agents_config = ConfigLoader.load_config("agents.yaml")
        self.tasks_config = ConfigLoader.load_config("tasks.yaml")
        self.llm = LLM(model="gemini/gemini-2.0-flash-exp", api_key=api_key)

        # Initialize agents and tasks
        self.agents = [self.researcher(), self.reporting_analyst()]
        self.tasks = [self.research_task(), self.reporting_task()]

    @agent
    def researcher(self) -> Agent:
        return Agent(
            **self.agents_config["researcher"],
            verbose=True,
            llm=self.llm,
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            **self.agents_config["reporting_analyst"],
            verbose=True,
            llm=self.llm,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            **self.tasks_config["research_task"],
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            **self.tasks_config["reporting_task"],
            output_file="output/report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        return Crew(
            agents=list(self.agents),
            tasks=list(self.tasks),
            process=Process.sequential,
            verbose=True,
        )
