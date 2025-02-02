from crewai import LLM, Agent, Crew, Process, Task
from dotenv import load_dotenv
import os

# Load API key from environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Initialize the LLM
llm = LLM(model="gemini/gemini-2.0-flash-exp", api_key=api_key)

researcher = Agent(
    role="Senior Data Researcher on {topic}",
    goal="Uncover cutting-edge developments in {topic}",
    backstory="""You're a seasoned researcher with a knack for uncovering the latest
    developments in {topic}. Known for your ability to find the most relevant
    information and present it in a clear and concise manner.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

research_task = Task(
    description="""
    Conduct a thorough research about {topic}
    Make sure you find any interesting and relevant information given
    the current year is 2024.
    """,
    expected_output="A list with 10 bullet points of the most relevant information about {topic}",
    agent=researcher,
)

reporting_analyst = Agent(
    role="{topic} Reporting Analyst",
    goal="Create detailed reports based on {topic} data analysis and research findings",
    backstory="""You're a meticulous analyst with a keen eye for detail. You're known for
    your ability to turn complex data into clear and concise reports, making
    it easy for others to understand and act on the information you provide.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)

reporting_task = Task(
    description="""
    Review the context you got and expand each topic into a full section for a report.
    Make sure the report is detailed and contains any and all relevant information.
    """,
    expected_output="""
    A fully fledge reports with the mains topics, each with a full section of information.
    Formatted as markdown without '```'
    
    """,
    agent=reporting_analyst,
    output_file="report.md",
)

crew = Crew(
    agents=[researcher, reporting_analyst],
    tasks=[research_task, reporting_task],
    verbose=True,
    process=Process.sequential,
)

crew.kickoff(inputs={"topic": "AI Agents"})
