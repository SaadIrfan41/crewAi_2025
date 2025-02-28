import os
from crewai import Crew, Process, LLM, Agent, Task
from mem0 import MemoryClient
from dotenv import load_dotenv

# Load API key from environment variables
load_dotenv()
# os.environ["MEM0_API_KEY"] = os.getenv("MEM0_API_KEY") or ""

# Initialize LLM
llm = LLM(model="gemini/gemini-2.0-flash-exp", api_key=os.getenv("GEMINI_API_KEY"))

# Initialize Mem0 client
memory_client = MemoryClient(api_key=os.getenv("MEM0_API_KEY"))


class ChatBot:
    def __init__(self):
        # Initialize the conversational agent
        self.chat_agent = Agent(
            role="Conversational AI Assistant",
            goal="Have meaningful and contextual conversations with users",
            backstory="""You are an AI-powered chatbot designed to assist users with their
                questions across various topics. Known for being approachable, you engage
                 in conversations with empathy, clarity, and a touch of humor""",
            verbose=True,
            allow_delegation=False,
            llm=llm,
        )

    def create_conversation_task(self, user_input):
        return Task(
            description=f"""Process the user's message: {user_input}. Maintain context from previous interactions and provide a precise, to-the-point response.""",
            expected_output="""A conversational response that answers the user's question clearly""",
            agent=self.chat_agent,
        )

    def chat(self, user_input, user_id="default_user"):
        # Store user interaction in memory
        memory_client.add([{"role": "user", "content": user_input}], user_id=user_id)

        # Create a crew with memory enabled
        crew = Crew(
            agents=[self.chat_agent],
            tasks=[self.create_conversation_task(user_input)],
            process=Process.sequential,
            memory=True,
            verbose=True,
            memory_config={
                "provider": "mem0",
                "config": {"user_id": user_id},
            },
        )

        # Get the response
        result = crew.kickoff()
        return result


def main():
    chatbot = ChatBot()
    print(
        "ChatBot: Hello! I'm your AI assistant. I can remember our conversation and maintain context. What would you like to discuss?"
    )

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["exit", "quit", "bye"]:
                print(
                    "\nChatBot: Goodbye! It was wonderful talking with you. Take care!"
                )
                break

            if not user_input:
                print("\nChatBot: I didn't catch that. Could you please say something?")
                continue

            response = chatbot.chat(user_input)
            print(f"\nChatBot: {response}")

        except KeyboardInterrupt:
            print("\n\nChatBot: Goodbye! Have a great day!")
            break
        except Exception as e:
            print(
                f"\nChatBot: I encountered an error: {str(e)}. Let's continue our conversation!"
            )


if __name__ == "__main__":
    main()
