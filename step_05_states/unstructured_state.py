from crewai.flow.flow import Flow, listen, start


class UnstructuredExampleFlow(Flow):
    @start()
    def first_method(self):
        # The state automatically includes an 'id' field
        print(f"State ID: {self.state['id']}")
        self.state["message"] = "Hello from unstructured flow"
        self.state["counter"] = 0

    @listen(first_method)
    def second_method(self):
        self.state["counter"] += 1
        self.state["message"] += " - updated"

    @listen(second_method)
    def third_method(self):
        self.state["counter"] += 1
        self.state["message"] += " - updated again"

        print(f"State after third_method: {self.state}")


flow = UnstructuredExampleFlow()
flow.kickoff()
