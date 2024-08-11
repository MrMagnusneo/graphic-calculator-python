import numpy as np
from scipy import integrate
from typing import Dict, List, Tuple, Any, Optional, Union
from sympy import sympify, diff, Symbol, SympifyError
import warnings

class GraphAnalyzer:
    def __init__(self, calculator: 'GraphCalculator', world_coords: Tuple[float, float, float, float]):
        self.calculator: 'GraphCalculator' = calculator
        self.world_coords: Tuple[float, float, float, float] = world_coords

    def analyze(self) -> Dict[str, Dict[str, Union[float, str, List[Union[float, Tuple[float, float]]], None]]]:
        results: Dict[str, Dict[str, Union[float, str, List[Union[float, Tuple[float, float]]], None]]] = {}
        x_min, y_min, x_max, y_max = self.world_coords
        x_range: np.ndarray = np.linspace(x_min, x_max, 10000)

        for name, function_data in self.calculator.functions.items():
            formula: str = function_data["formula"]
            y_values: np.ndarray = self.safe_calculate(formula, x_range)

            if len(y_values) > 0:
                results[name] = {
                    "min": float(np.nanmin(y_values)),
                    "max": float(np.nanmax(y_values)),
                    "mean": float(np.nanmean(y_values)),
                    "median": float(np.nanmedian(y_values)),
                    "std_dev": float(np.nanstd(y_values)),
                    "roots": self.find_roots(formula, x_range, y_values),
                    "extrema": self.find_extrema(x_range, y_values),
                    "inflection_points": self.find_inflection_points(formula, x_range),
                    "area_under_curve": self.calculate_area(formula, x_min, x_max),
                    "derivative": self.get_derivative(formula),
                    "arc_length": self.calculate_arc_length(formula, x_min, x_max),
                }

        return results

    def safe_calculate(self, formula: str, x_values: np.ndarray) -> np.ndarray:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            y_values: np.ndarray = np.array([self.calculator.calculate(formula, x) for x in x_values])
        return y_values[np.isfinite(y_values)]

    def find_roots(self, formula: str, x_range: np.ndarray, y_values: np.ndarray) -> Optional[List[float]]:
        try:
            roots: List[float] = []
            for i in range(len(y_values) - 1):
                if y_values[i] * y_values[i+1] <= 0:
                    root = self.binary_search_root(formula, x_range[i], x_range[i+1], y_values[i], y_values[i+1])
                    if root is not None:
                        roots.append(round(root, 4))
            return roots if roots else None
        except Exception:
            return None

    def binary_search_root(self, formula: str, x1: float, x2: float, y1: float, y2: float, tolerance: float = 1e-6) -> Optional[float]:
        try:
            while abs(x2 - x1) > tolerance:
                x_mid: float = (x1 + x2) / 2
                y_mid: float = self.calculator.calculate(formula, x_mid)
                if y_mid is None or not np.isfinite(y_mid):
                    return None
                if y_mid * y1 <= 0:
                    x2, y2 = x_mid, y_mid
                else:
                    x1, y1 = x_mid, y_mid
            return (x1 + x2) / 2
        except Exception:
            return None

    def find_extrema(self, x_range: np.ndarray, y_values: np.ndarray) -> Optional[List[Tuple[float, float]]]:
        try:
            extrema: List[Tuple[float, float]] = []
            for i in range(1, len(y_values) - 1):
                if (y_values[i-1] < y_values[i] > y_values[i+1]) or (y_values[i-1] > y_values[i] < y_values[i+1]):
                    extrema.append((round(float(x_range[i]), 4), round(float(y_values[i]), 4)))
            return extrema if extrema else None
        except Exception:
            return None

    def find_inflection_points(self, formula: str, x_range: np.ndarray) -> Optional[List[Tuple[float, float]]]:
        try:
            x: Symbol = Symbol('x')
            expr = sympify(formula)
            second_derivative = diff(expr, x, 2)
            inflection_points: List[Tuple[float, float]] = []

            for i in range(len(x_range) - 1):
                y1 = self.safe_sympy_eval(second_derivative, x_range[i])
                y2 = self.safe_sympy_eval(second_derivative, x_range[i+1])
                if y1 is not None and y2 is not None and y1 * y2 <= 0:
                    x_inflection = self.binary_search_root(str(second_derivative), x_range[i], x_range[i+1], y1, y2)
                    if x_inflection is not None:
                        y_inflection = self.calculator.calculate(formula, x_inflection)
                        if y_inflection is not None and np.isfinite(y_inflection):
                            inflection_points.append((round(x_inflection, 4), round(y_inflection, 4)))
            return inflection_points if inflection_points else None
        except (SympifyError, Exception):
            return None

    def safe_sympy_eval(self, expr: Symbol, value: float) -> Optional[float]:
        try:
            result: float = float(expr.subs('x', value))
            return result if np.isfinite(result) else None
        except Exception:
            return None

    def calculate_area(self, formula: str, x_min: float, x_max: float) -> Optional[float]:
        try:
            def func(x: float) -> float:
                result = self.calculator.calculate(formula, x)
                return result if result is not None and np.isfinite(result) else 0
            
            area, _ = integrate.quad(func, x_min, x_max)
            return round(area, 4) if np.isfinite(area) else None
        except Exception:
            return None

    def get_derivative(self, formula: str) -> Optional[str]:
        try:
            x: Symbol = Symbol('x')
            expr = sympify(formula)
            derivative = diff(expr, x)
            return str(derivative)
        except (SympifyError, Exception):
            return None

    def calculate_arc_length(self, formula: str, x_min: float, x_max: float) -> Optional[float]:
        try:
            x: Symbol = Symbol('x')
            expr = sympify(formula)
            derivative = diff(expr, x)

            def integrand(x: float) -> float:
                dy_dx = self.safe_sympy_eval(derivative, x)
                return np.sqrt(1 + dy_dx**2) if dy_dx is not None else 0

            arc_length, _ = integrate.quad(integrand, x_min, x_max)
            return round(arc_length, 4) if np.isfinite(arc_length) else None
        except Exception:
            return None
