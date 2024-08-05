from turtle import *
from math import *
screensize(0.8,0.8)
setup(width=0.5, height=0.5, startx=1, starty=None)
tracer(0)
up()
m = 95 #масштаб
t = 0.01 #точность
s = -500 #начало
e = 500 #конец
for i in range(s, e):
    x = i*t
    y = (x)**3*sin((x)**2) #формула графика
    goto(x*m,y*m)
    down()
update()
done()
