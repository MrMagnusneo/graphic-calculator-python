from typing import Optional, Dict, Any
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from modules.graph_calculator import GraphCalculator
from modules.graph_plotter import GraphPlotter
from modules.function_input import FunctionInputDialog
from modules.graph_analysis import GraphAnalyzer
import threading
import queue

class GraphCalculatorGUI:
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("График Калькулятор")
        self.master.geometry("1400x600")

        self.calculator = GraphCalculator()
        self.current_color: Optional[str] = "#000000"
        
        self.create_widgets()
        
        self.plotter = GraphPlotter(self.canvas)

    def create_widgets(self) -> None:
        self.main_frame = ttk.Frame(self.master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_function_frame()
        self.create_canvas()
        self.create_control_frame()

    def create_function_frame(self) -> None:
        self.function_frame = ttk.Frame(self.main_frame)
        self.function_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.function_button = ttk.Button(self.function_frame, text="Добавить функцию", command=self.open_function_dialog)
        self.function_button.pack()

        self.color_button = ttk.Button(self.function_frame, text="Выбрать цвет", command=self.choose_color)
        self.color_button.pack()

        self.function_listbox = tk.Listbox(self.function_frame, width=40, height=10)
        self.function_listbox.pack()
        self.function_listbox.bind('<Double-1>', self.on_function_double_click)

        self.remove_button = ttk.Button(self.function_frame, text="Удалить", command=self.remove_function)
        self.remove_button.pack()

        self.clear_button = ttk.Button(self.function_frame, text="Очистить все", command=self.clear_all)
        self.clear_button.pack()
        
        self.analyze_button = ttk.Button(self.function_frame, text="Анализировать", command=self.analyze_graphs)
        self.analyze_button.pack()

    def create_canvas(self) -> None:
        self.canvas = tk.Canvas(self.main_frame, width=600, height=400)
        self.canvas.pack(side="left", fill=tk.BOTH, expand=True)

    def create_control_frame(self) -> None:
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(side="right", fill="y", padx=10, pady=10)

        self.zoom_in_button = ttk.Button(self.control_frame, text="Увеличить", command=self.zoom_in)
        self.zoom_in_button.pack()

        self.zoom_out_button = ttk.Button(self.control_frame, text="Уменьшить", command=self.zoom_out)
        self.zoom_out_button.pack()

        self.move_frame = ttk.Frame(self.control_frame)
        self.move_frame.pack()

        self.move_up = ttk.Button(self.move_frame, text="↑", command=lambda: self.move(0, 1))
        self.move_up.grid(row=0, column=1)

        self.move_left = ttk.Button(self.move_frame, text="←", command=lambda: self.move(-1, 0))
        self.move_left.grid(row=1, column=0)

        self.move_right = ttk.Button(self.move_frame, text="→", command=lambda: self.move(1, 0))
        self.move_right.grid(row=1, column=2)

        self.move_down = ttk.Button(self.move_frame, text="↓", command=lambda: self.move(0, -1))
        self.move_down.grid(row=2, column=1)

        self.coords_label = ttk.Label(self.control_frame, text="")
        self.coords_label.pack(pady=10)

    def open_function_dialog(self) -> None:
        dialog = FunctionInputDialog(self.master)
        result = dialog.show()
        if result:
            self.add_function(result)

    def choose_color(self) -> None:
        self.current_color = colorchooser.askcolor()[1]

    def add_function(self, formula: str) -> None:
        if formula:
            name = f"f{len(self.calculator.functions) + 1}(x)"
            formula = formula.replace('^', '**')
            self.calculator.add_function(name, formula, self.current_color)
            self.function_listbox.insert(tk.END, f"{name}: {formula} ({self.current_color})")
            self.plotter.plot_function(self.calculator, name, formula, self.current_color)
            self.plotter.redraw()

    def remove_function(self) -> None:
        selection = self.function_listbox.curselection()
        if selection:
            index = selection[0]
            name = self.function_listbox.get(index).split(":")[0]
            self.calculator.remove_function(name)
            self.function_listbox.delete(index)
            self.redraw_all_functions()

    def clear_all(self) -> None:
        self.calculator.functions.clear()
        self.function_listbox.delete(0, tk.END)
        self.plotter.clear()
        self.plotter.redraw()

    def redraw_all_functions(self) -> None:
        self.plotter.clear()
        for name, function_data in self.calculator.functions.items():
            self.plotter.plot_function(self.calculator, name, function_data["formula"], function_data["color"])
        self.plotter.redraw()
        self.update_coords_label()

    def zoom_in(self) -> None:
        self.plotter.zoom(0.8)
        self.redraw_all_functions()

    def zoom_out(self) -> None:
        self.plotter.zoom(1.25)
        self.redraw_all_functions()

    def move(self, dx: float, dy: float) -> None:
        self.plotter.move(dx, dy)
        self.redraw_all_functions()

    def update_coords_label(self) -> None:
        coords = self.plotter.get_world_coords()
        self.coords_label.config(text=f"X: [{coords[0]:.2f}, {coords[2]:.2f}]\nY: [{coords[1]:.2f}, {coords[3]:.2f}]")
    
    def analyze_graphs(self) -> None:
        if not self.calculator.functions:
            messagebox.showinfo("Анализ", "Нет функций для анализа.")
            return

        progress_window = tk.Toplevel(self.master)
        progress_window.title("Анализ")
        progress_label = ttk.Label(progress_window, text="Выполняется анализ...")
        progress_label.pack(padx=20, pady=20)
        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
        progress_bar.pack(padx=20, pady=10)
        progress_bar.start()

        result_queue = queue.Queue()

        def analyze_thread():
            analyzer = GraphAnalyzer(self.calculator, self.plotter.get_world_coords())
            results = analyzer.analyze()
            result_queue.put(results)

        threading.Thread(target=analyze_thread, daemon=True).start()

        def check_result():
            try:
                results = result_queue.get_nowait()
                progress_window.destroy()
                self.show_analysis_results(results)
            except queue.Empty:
                self.master.after(100, check_result)


        self.master.after(100, check_result)

    def show_analysis_results(self, results: Dict[str, Dict[str, Any]]) -> None:
        analysis_window = tk.Toplevel(self.master)
        analysis_window.title("Результаты анализа")
        analysis_window.geometry("700x700")

        notebook = ttk.Notebook(analysis_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for name, data in results.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=name)

            text_widget = tk.Text(frame, wrap=tk.WORD, width=80, height=25)
            text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            text_widget.insert(tk.END, f"Анализ функции {name}:\n\n")
            text_widget.insert(tk.END, f"Минимум: {data['min']:.4f}\n")
            text_widget.insert(tk.END, f"Максимум: {data['max']:.4f}\n")
            text_widget.insert(tk.END, f"Среднее: {data['mean']:.4f}\n")
            text_widget.insert(tk.END, f"Медиана: {data['median']:.4f}\n")
            text_widget.insert(tk.END, f"Стандартное отклонение: {data['std_dev']:.4f}\n\n")

            text_widget.insert(tk.END, f"Корни: {', '.join(map(str, data['roots'])) if data['roots'] else 'Не найдены'}\n")
            text_widget.insert(tk.END, f"Экстремумы: {', '.join(map(str, data['extrema'])) if data['extrema'] else 'Не найдены'}\n")
            text_widget.insert(tk.END, f"Точки перегиба: {', '.join(map(str, data['inflection_points'])) if data['inflection_points'] else 'Не найдены'}\n\n")

            area_under_curve = data.get('area_under_curve')
            if area_under_curve is not None:
                area_text = f"{area_under_curve:.4f}"
            else:
                area_text = "Не удалось вычислить"
            text_widget.insert(tk.END, f"Площадь под кривой: {area_text}\n")

            text_widget.insert(tk.END, f"Производная: {data['derivative'] if data['derivative'] is not None else 'Не удалось вычислить'}\n")

            if 'arc_length' in data:
                arc_length = data['arc_length']
                if arc_length is not None:
                    arc_length_text = f"{arc_length:.4f}"
                else:
                    arc_length_text = "Не удалось вычислить"
                text_widget.insert(tk.END, f"Длина дуги: {arc_length_text}\n")

            text_widget.config(state=tk.DISABLED)

        save_button = ttk.Button(analysis_window, text="Сохранить результаты", command=lambda: self.save_analysis_results(results))
        save_button.pack(pady=10)
        
    def on_function_double_click(self, event):
        selection = self.function_listbox.curselection()
        if selection:
            index = selection[0]
            function_info = self.function_listbox.get(index)
            name = function_info.split(":")[0]
            formula = function_info.split(":")[1].split("(")[0].strip().replace('^', '**')
            color = function_info.split("(")[-1].strip(")")
            
            self.plotter.clear()
            self.plotter.plot_function(self.calculator, name, formula, color)
            self.plotter.redraw()
            
    def save_analysis_results(self, results: Dict[str, Dict[str, Any]]) -> None:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                for name, data in results.items():
                    file.write(f"Анализ функции {name}:\n\n")
                    file.write(f"Минимум: {data['min']:.4f}\n")
                    file.write(f"Максимум: {data['max']:.4f}\n")
                    file.write(f"Среднее: {data['mean']:.4f}\n")
                    file.write(f"Медиана: {data['median']:.4f}\n")
                    file.write(f"Стандартное отклонение: {data['std_dev']:.4f}\n\n")
                    file.write(f"Корни: {', '.join(map(str, data['roots'])) if data['roots'] else 'Не найдены'}\n")
                    file.write(f"Экстремумы: {', '.join(map(str, data['extrema'])) if data['extrema'] else 'Не найдены'}\n")
                    file.write(f"Точки перегиба: {', '.join(map(str, data['inflection_points'])) if data['inflection_points'] else 'Не найдены'}\n\n")
                    
                    area_under_curve = data.get('area_under_curve')
                    if area_under_curve is not None:
                        area_text = f"{area_under_curve:.4f}"
                    else:
                        area_text = "Не удалось вычислить"
                    file.write(f"Площадь под кривой: {area_text}\n")
                    
                    file.write(f"Производная: {data['derivative'] if data['derivative'] is not None else 'Не удалось вычислить'}\n")
                    
                    if 'arc_length' in data:
                        arc_length = data['arc_length']
                        if arc_length is not None:
                            arc_length_text = f"{arc_length:.4f}"
                        else:
                            arc_length_text = "Не удалось вычислить"
                        file.write(f"Длина дуги: {arc_length_text}\n")
                    
                    file.write("\n\n")
            messagebox.showinfo("Сохранение", "Результаты анализа успешно сохранены.")