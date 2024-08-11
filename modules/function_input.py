import tkinter as tk
from tkinter import ttk

class FunctionInputDialog:
    def __init__(self, parent):
        self.parent = parent
        self.result = None
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Ввод функции")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.create_widgets()

    def create_widgets(self):
        self.function_entry = ttk.Entry(self.dialog, width=40)
        self.function_entry.pack(pady=10)

        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.BOTH, expand=True)

        buttons = [
            '7', '8', '9', '/', 'C',
            '4', '5', '6', '*', '(',
            '1', '2', '3', '-', ')',
            '0', '.', '^', '+', 'x',
            'sin', 'cos', 'tan', 'log', 'exp'
        ]

        row, col = 0, 0
        for button in buttons:
            ttk.Button(button_frame, text=button, width=5,
                       command=lambda x=button: self.on_button_click(x)).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 4:
                col = 0
                row += 1

        ttk.Button(self.dialog, text="OK", command=self.on_ok).pack(pady=10)

    def on_button_click(self, value):
        if value == 'C':
            self.function_entry.delete(0, tk.END)
        else:
            self.function_entry.insert(tk.END, value)

    def on_ok(self):
        self.result = self.function_entry.get().replace('^', '**')  
        self.dialog.destroy()

    def show(self):
        self.parent.wait_window(self.dialog)
        return self.result