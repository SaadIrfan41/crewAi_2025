from crewai import LLM, Agent, Process, Task, Crew

# from crewai_tools import CSVSearchTool
# from crewai.knowledge.source.crew_docling_source import CrewDoclingSource
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
from crewai.knowledge.source.csv_knowledge_source import CSVKnowledgeSource

# from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# llm = LLM(model="ollama/qwen2.5:3b", base_url="http://localhost:11434")
llm = LLM(model="gemini/gemini-2.0-flash-exp", api_key=api_key)

content_source = PDFKnowledgeSource(
    file_paths=["students_data.pdf"],
)
# content_source = PDFKnowledgeSource(
#     file_paths=["saadirfan_cv.pdf"],
# )

# tool = CSVSearchTool(
#     csv="students_data.csv",
#     config=dict(
#         llm=dict(
#             provider="google",  # or google, openai, anthropic, llama2, ...
#             config=dict(
#                 model="gemini-2.0-flash-exp",
#                 api_key=api_key,
#                 # temperature=0.5,
#                 # top_p=1,
#                 # stream=true,
#             ),
#         ),
#         # llm=dict(
#         #     provider="ollama",  # or google, openai, anthropic, llama2, ...
#         #     config=dict(
#         #         model="qwen2.5:3b",
#         #         # temperature=0.5,
#         #         # top_p=1,
#         #         # stream=true,
#         #     ),
#         # ),
#         embedder=dict(
#             provider="ollama",  # or openai, ollama, ...
#             config=dict(
#                 model="nomic-embed-text:latest",
#             ),
#         ),
#     ),
# )


# agent1 researcher
# researcher = Agent(
#     role="Expert Data Analyst",
#     goal="""Extract relevant data from the csv file and structure them as instructed""",
#     backstory="""You are an expert data analyst for extracting information from csv files as instructed in the task description""",
#     allow_delegation=False,
#     verbose=True,
#     tools=[tool],
#     llm=llm,
# )


# Create tasks
# task1 = Task(
#     description="""Extract relevant data asked by the user .
#      Question:{question}""",
#     expected_output="output the question in plain text",
#     agent=researcher,
#     output_file="students_data.md",
# )

# task2 = Task(
#     description="""Using the structured data and insights provided by the Expert Data Analyst agent, output all the students and their details in markdown format""",
#     expected_output="Technical report and explanation of at least 1000 words",
#     agent=writer,
# )

agent = Agent(
    role="About Students",
    goal="You know everything about the Students.",
    backstory="""You are a master at understanding Students and their content.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
task = Task(
    description="Extract the required columns and present them in a list format.: {question}",
    expected_output="An answer to the question.",
    agent=agent,
    # output_file="cv.md",
)

# Instantiate your crew with a sequential process
# crew = Crew(
#     agents=[researcher],
#     tasks=[task1],
#     verbose=True,
# )
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    knowledge_sources=[content_source],
    embedder={
        "provider": "google",
        "config": {
            "model": "models/text-embedding-004",
            "api_key": api_key,
        },
    },
    # embedder={
    #     "provider": "ollama",
    #     "config": {
    #         "model": "nomic-embed-text:latest",
    #     },
    # },
)

while True:
    question = input("Enter your question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        print("Goodbye!")
        break

    result = crew.kickoff(inputs={"question": question})
