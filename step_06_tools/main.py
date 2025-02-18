#!/usr/bin/env python
from crew import CalculatorCrew


# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the calculator crew.
    """

    inputs = {
        "addition_number1": 5.75,
        "addition_number2": 3.25,
        "subtraction_number1": 10,
        "subtraction_number2": 4,
        "multiplication_number1": 6,
        "multiplication_number2": 7,
        # "division_number1": 15,
        # "division_number2": 3,
    }

    result = CalculatorCrew().crew().kickoff(inputs=inputs)
    print(f"Result: {result}")


if __name__ == "__main__":
    run()
