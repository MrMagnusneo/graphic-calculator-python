import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def calculate(func, x):
    """Evaluate a symbolic function at a given point"""
    x_sym = sp.symbols('x')
    func_sym = sp.sympify(func)
    return sp.lambdify(x_sym, func_sym)(x)

def plot_func(func, x_range):
    """Plot a function over a given range"""
    x = np.linspace(x_range[0], x_range[1], 400)
    y = calculate(func, x)
    plt.clf()  # Clear the current figure
    plt.plot(x, y)
    plt.title(f"y = {func}")
    plt.draw()  # Update the plot

def main():
    """Main entry point"""
    func_str = input("Enter a function expression (e.g., 'x**2 + 2*x + 1'): ")
    x_range = [-10, 10] # x ranges
    plot_func(func_str, x_range)
    plt.show()

if __name__ == "__main__":
    main()
