from turtle import *
from math import *

# Set up the screen
screensize(0.8, 0.8)
setup(width=0.5, height=0.5, startx=1, starty=None)

# Set up the turtle
tracer(0)
up()

# Define constants
SCALE = 95
PRECISION = 0.01
START = -500
END = 500

# Define a function to plot a graph
def plot_graph(formula, color):
    down()
    pencolor(color)
    for x in range(START, END):
        y = eval(formula)
        goto(x * SCALE, y * SCALE)
    up()

# Plot multiple graphs
plot_graph("x**3 * sin(x**2)", "blue")
plot_graph("x**2 * cos(x)", "red")
plot_graph("x * sin(x**3)", "green")

# Add a legend
goto(-200, 200)
write("Синий: y = x^3 * sin(x^2)", align="left", font=("Arial", 12, "normal"))
goto(-200, 180)
write("Красный: y = x^2 * cos(x)", align="left", font=("Arial", 12, "normal"))
goto(-200, 160)
write("Зеленый: y = x * sin(x^3)", align="left", font=("Arial", 12, "normal"))

# Update and close the turtle graphics window
update()
done()
