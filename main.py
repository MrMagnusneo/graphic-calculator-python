import tkinter as tk
from modules.gui import GraphCalculatorGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphCalculatorGUI(root)
    root.mainloop()