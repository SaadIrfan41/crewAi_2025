from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel


class ExampleState(BaseModel):
    # Note: 'id' field is automatically added to all states
    counter: int = 0
    message: str = ""

    # # Implementing __getitem__ to support dictionary-like access
    # def __getitem__(self, key):
    #     # Return the attribute value if it exists
    #     if key in self.model_dump():
    #         return self.model_dump()[key]
    #     else:
    #         raise KeyError(f"Key '{key}' not found in the state.")


class StructuredExampleFlow(Flow[ExampleState]):
    @start()
    def first_method(self):
        # Access the auto-generated ID if needed
        state_id = getattr(self.state, "id", None)
        print(f"State ID: {state_id}")
        self.state.message = "Hello from structured flow"

    @listen(first_method)
    def second_method(self):
        self.state.counter += 1
        self.state.message += " - updated"

    @listen(second_method)
    def third_method(self):
        self.state.counter += 1
        self.state.message += " - updated again"

        print(f"State after third_method: {self.state}")


flow = StructuredExampleFlow()
flow.kickoff()
