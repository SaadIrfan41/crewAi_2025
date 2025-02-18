import asyncio
from crewai.flow.flow import Flow, listen, start, and_


class AndExampleFlow(Flow):
    @start()
    def start_method(self):
        print("Start Flow")
        self.state["start"] = "Hello from the start method"
        # return "Hello from the start method"

    @listen(start_method)
    async def second_method(self):
        await asyncio.sleep(1)
        print("Second Flow")
        self.state["second"] = "Hello from the second method"
        # return "Hello from the second method"

    @listen(second_method)
    async def third_method(self):
        await asyncio.sleep(2)
        print("Third Flow")
        self.state["third"] = "Hello from the third method"
        # return "Hello from the third method"

    @listen(second_method)
    async def fourth_method(self):
        await asyncio.sleep(3)
        print("fourth Flow")
        self.state["forth"] = "Hello from the forth method"
        # return "Hello from the fourth method"

    @listen(and_(start_method, second_method, third_method, fourth_method))
    def logger(self):
        print(f"Logger Start: {self.state['start']}")
        print(f"Logger Second: {self.state['second']}")
        print(f"Logger Third: {self.state['third']}")
        print(f"Logger Forth: {self.state['forth']}")


flow = AndExampleFlow()
flow.kickoff()
