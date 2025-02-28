from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
import os
from dotenv import load_dotenv

# Create a PDF knowledge source
pdf_source = PDFKnowledgeSource(
    file_paths=[
        "saadirfan_cv.pdf",
    ]
)


# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Create an LLM with a temperature of 0 to ensure deterministic outputs
llm = LLM(model="gemini/gemini-2.0-flash-exp", temperature=0)

# Create an agent with the knowledge store
agent = Agent(
    role="PDF Knowledge Expert",
    goal="Answer questions accurately based on PDF content",
    backstory="""You are an expert at analyzing PDF documents and providing accurate information from them. 
    If you cannot find the answer in the provided PDF, you will clearly state that you don't know.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
    knowledge_sources=[pdf_source],
    embedder_config={
        "provider": "google",
        "config": {
            "model": "models/text-embedding-004",
            "api_key": GEMINI_API_KEY,
        },
    },
)
task = Task(
    description="Based on the PDF content, answer this question: {question}. If the answer cannot be found in the PDF, respond with 'I don't know.'",
    expected_output="A factual answer from the PDF or 'I don't know' if information is not available.",
    agent=agent,
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True,
    process=Process.sequential,
    # knowledge_sources=[pdf_source], # Enable knowledge by adding the sources here. You can also add more sources to the sources list.
    #  embedder={
    #     "provider": "google",
    #     "config": {
    #         "model": "models/text-embedding-004",
    #         "api_key": GEMINI_API_KEY,
    #     }
    # } # Enable embedding by adding the embedder here.
)

# result = crew.kickoff(inputs={"question": "What city does John live in and how old is he?"})
result = crew.kickoff(
    inputs={
        "question": "What city does Saad live in and how many languages does he speak?"
    }
)
