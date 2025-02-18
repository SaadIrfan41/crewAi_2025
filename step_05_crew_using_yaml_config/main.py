#!/usr/bin/env python
import warnings

from crew import LatestAiDevelopmentCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    inputs = {"topic": "Nvidia Ces 2025"}
    LatestAiDevelopmentCrew().crew().kickoff(inputs=inputs)


run()
