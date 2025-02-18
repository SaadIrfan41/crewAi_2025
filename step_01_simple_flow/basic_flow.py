from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv
from litellm import completion
import os

# Load API key from environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


class ExampleFlow(Flow):
    model = "gemini/gemini-2.0-flash-exp"

    @start()
    def generate_city(self):
        print("Starting flow")

        # Each flow state automatically gets a unique ID
        print(f"Flow State ID: {self.state['id']}")

        response = completion(
            model=self.model,
            api_key=api_key,
            messages=[
                {
                    "role": "user",
                    "content": "Return the name of a random city in the world.Just give me a name.",
                },
            ],
        )
        # choices = getattr(response, "choices", [])
        # if choices and isinstance(choices, list) and len(choices) > 0:
        #     # Access the first item safely
        #     message = getattr(choices[0], "message", {})
        #     # Now check for 'content' inside 'message'
        #     content = getattr(message, "content", None)
        # else:
        #     content = "Peshawar"

        # random_city = content
        random_city = response["choices"][0]["message"]["content"]  # type: ignore

        print(f"Random City: {random_city}")

        return random_city

    @listen(generate_city)
    def generate_fun_fact(self, random_city):
        response = completion(
            model=self.model,
            api_key=api_key,
            messages=[
                {
                    "role": "user",
                    "content": f"Tell me a fun fact about {random_city}",
                },
            ],
        )

        fun_fact = response["choices"][0]["message"]["content"]  # type: ignore
        return fun_fact


flow = ExampleFlow()
result = flow.kickoff()

print(f"Generated fun fact: {result}")
