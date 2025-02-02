from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from dotenv import load_dotenv
import os

# Load API key from environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the LLM
llm = LLM(model="gemini/gemini-2.0-flash-exp", api_key=api_key)
# llm = LLM(model="ollama/qwen2.5:3b", base_url="http://localhost:11434")


@CrewBase
class LatestAiDevelopmentCrew:
    """LatestAiDevelopment crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],  # type: ignore
            verbose=True,
            llm=llm,
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["reporting_analyst"],  # type: ignore
            verbose=True,
            llm=llm,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],  # type: ignore
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config["reporting_task"],  # type: ignore
            output_file="output/report.md",  # This is the file that will be contain the final report.
        )

    @crew
    def crew(self) -> Crew:
        """Creates the LatestAiDevelopment crew"""
        return Crew(
            agents=self.agents,  # type: ignore  # Automatically created by the @agent decorator
            tasks=self.tasks,  # type: ignore  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
