import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from typing import Tuple

class GraphPlotter:
    def __init__(self, master):
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.world_coords = (-10, -10, 10, 10)
        self.setup_plot()

    def setup_plot(self):
        self.ax.clear()
        self.ax.set_xlim(self.world_coords[0], self.world_coords[2])
        self.ax.set_ylim(self.world_coords[1], self.world_coords[3])
        self.ax.grid(True)
        self.ax.axhline(y=0, color='k')
        self.ax.axvline(x=0, color='k')

    def plot_function(self, calculator: 'GraphCalculator', name: str, formula: str, color: str) -> None:
        x = np.linspace(self.world_coords[0], self.world_coords[2], 1000)
        y = [calculator.calculate(formula, xi) for xi in x]
        self.ax.plot(x, y, label=name, color=color)
        self.ax.legend()

    def clear(self) -> None:
        self.setup_plot()

    def redraw(self):
        self.canvas.draw()

    def zoom(self, factor: float) -> None:
        x1, y1, x2, y2 = self.world_coords
        center_x, center_y = (x1 + x2) / 2, (y1 + y2) / 2
        new_width, new_height = (x2 - x1) * factor, (y2 - y1) * factor
        new_x1, new_y1 = center_x - new_width / 2, center_y - new_height / 2
        new_x2, new_y2 = center_x + new_width / 2, center_y + new_height / 2
        self.world_coords = (new_x1, new_y1, new_x2, new_y2)
        self.setup_plot()

    def move(self, dx: float, dy: float) -> None:
        x1, y1, x2, y2 = self.world_coords
        move_x = (x2 - x1) * dx * 0.1
        move_y = (y2 - y1) * dy * 0.1
        self.world_coords = (x1 + move_x, y1 + move_y, x2 + move_x, y2 + move_y)
        self.setup_plot()

    def get_world_coords(self) -> Tuple[float, float, float, float]:
        return self.world_coords