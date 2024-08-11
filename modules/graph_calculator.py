from typing import Dict, Any, Optional
import math

class GraphCalculator:
    def __init__(self):
        self.functions: Dict[str, Dict[str, Any]] = {}
        self.constants: Dict[str, float] = {
            "pi": math.pi,
            "e": math.e
        }
        self.operations: Dict[str, Any] = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,
            "exp": math.exp,
            "sqrt": math.sqrt,
            "abs": abs
        }

    def add_function(self, name: str, formula: str, color: str) -> None:
        self.functions[name] = {"formula": formula, "color": color}

    def remove_function(self, name: str) -> None:
        if name in self.functions:
            del self.functions[name]

    def calculate(self, formula: str, x: float) -> Optional[float]:
        try:
            return eval(formula, {"__builtins__": None}, 
                        {**self.constants, **self.operations, "x": x})
        except:
            return None