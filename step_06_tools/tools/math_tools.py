from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class TwoNumbersInput(BaseModel):
    number1: float = Field(..., description="First number for operation")
    number2: float = Field(..., description="Second number for operation")


class AddNumbersTool(BaseTool):
    name: str = "Add Numbers Tool"
    description: str = "Adds two numbers together"
    args_schema: type[BaseModel] = TwoNumbersInput

    def _run(self, number1: float, number2: float) -> float:
        """Adds two numbers together."""
        return number1 + number2


class SubtractNumbersTool(BaseTool):
    name: str = "Subtract Numbers Tool"
    description: str = "Subtracts the second number from the first number"
    args_schema: type[BaseModel] = TwoNumbersInput

    def _run(self, number1: float, number2: float) -> float:
        """Subtracts number2 from number1."""
        return number1 - number2


class MultiplyNumbersTool(BaseTool):
    name: str = "Multiply Numbers Tool"
    description: str = "Multiplies two numbers together"
    args_schema: type[BaseModel] = TwoNumbersInput

    def _run(self, number1: float, number2: float) -> float:
        """Multiplies two numbers."""
        return number1 * number2


class DivideNumbersTool(BaseTool):
    name: str = "Divide Numbers Tool"
    description: str = "Divides the first number by the second number"
    args_schema: type[BaseModel] = TwoNumbersInput

    def _run(self, number1: float, number2: float) -> float:
        """Divides number1 by number2."""
        if number2 == 0:
            raise ValueError("Cannot divide by zero")
        return number1 / number2
