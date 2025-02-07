from crewai.flow.flow import Flow, listen, or_, start
import time


class OrExampleFlow(Flow):
    @start()
    def start_method(self):
        print("Start Flow")
        return "Hello from the start method"

    @listen(start_method)
    def second_method(self):
        time.sleep(1)
        print("Second Flow")
        return "Hello from the second method"

    @listen(second_method)
    def third_method(self):
        time.sleep(2)
        print("Third Flow")
        return "Hello from the third method"

    @listen(second_method)
    def fourth_method(self):
        time.sleep(3)
        print("fourth Flow")
        return "Hello from the fourth method"

    @listen(or_(start_method, second_method, third_method, fourth_method))
    def logger(self, result):
        print(f"Logger: {result}")


flow = OrExampleFlow()
flow.kickoff()
