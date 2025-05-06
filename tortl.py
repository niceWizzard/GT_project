import turtle

t = turtle.Turtle()

s = turtle.Screen()
colors =[ "blue", "green", "purple", "orange", "darkred", "lightblue", "darkgreen", "cadetblue", "pink"]
s.bgcolor("black")
t.pensize(2)
t.speed(0)

for x in range(90):
    t.pencolor(colors[x % 8])
    t.forward(x)
    t.left(59)
    turtle.hideturtle()
