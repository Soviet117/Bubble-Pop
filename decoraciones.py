import turtle
import random
import math

ANCHO, ALTO = 900, 650
COLOR_AGUA_SUPERIOR = "#0E5B7A"
COLOR_ARENA = "#D2B48C"
COLOR_ALGAS = "#2E8B57"
COLOR_ALGAS_CLARO = "#3CB371"

lista_peces = []
lista_burbujas_deco = []
lista_algas = []
juego_terminado = False

def dibujar_gradiente():
    grad = turtle.Turtle()
    grad.hideturtle()
    grad.speed(0)
    grad.penup()
    pasos = 50
    for i in range(pasos):
        proporcion = i / pasos
        r = int(2 + (14 - 2) * proporcion)
        g = int(0x1B + (0x5B - 0x1B) * proporcion)
        b = int(0x2B + (0x7A - 0x2B) * proporcion)
        color = f"#{r:02x}{g:02x}{b:02x}"
        grad.goto(-ANCHO//2, ALTO//2 - (i * ALTO/pasos))
        grad.pendown()
        grad.color(color)
        grad.begin_fill()
        for _ in range(2):
            grad.forward(ANCHO)
            grad.right(90)
            grad.forward(ALTO/pasos)
            grad.right(90)
        grad.end_fill()
        grad.penup()
    grad.hideturtle()

def dibujar_arena():
    arena = turtle.Turtle()
    arena.hideturtle()
    arena.speed(0)
    arena.penup()
    arena.goto(-ANCHO//2, -250)
    arena.color(COLOR_ARENA)
    arena.begin_fill()
    arena.goto(ANCHO//2, -250)
    arena.goto(ANCHO//2, -ALTO//2)
    arena.goto(-ANCHO//2, -ALTO//2)
    arena.end_fill()
    arena.goto(-ANCHO//2, -250)
    arena.color("#F5DEB3")
    arena.pensize(3)
    for x in range(-ANCHO//2, ANCHO//2, 10):
        arena.goto(x, -250 + 5 * math.sin(x * 0.05))
    for _ in range(30):
        x = random.randint(-ANCHO//2, ANCHO//2)
        y = random.randint(-280, -255)
        arena.goto(x, y)
        arena.dot(3, "#EEDDAA")
    arena.hideturtle()

def dibujar_alga(x, altura, grosor=2):
    alga = turtle.Turtle()
    alga.hideturtle()
    alga.speed(0)
    alga.penup()
    alga.goto(x, -250)
    alga.pendown()
    alga.pensize(grosor)
    alga.color(COLOR_ALGAS)
    for i in range(altura // 5):
        segmento_y = -250 + i * 5
        offset_x = 5 * math.sin(i * 0.8)
        alga.goto(x + offset_x, segmento_y)
    alga.color(COLOR_ALGAS_CLARO)
    alga.pensize(1)
    alga.penup()
    alga.goto(x, -250)
    alga.pendown()
    for i in range(altura // 5):
        segmento_y = -250 + i * 5
        offset_x = -3 * math.sin(i * 0.7)
        alga.goto(x + offset_x, segmento_y)
    lista_algas.append(alga)

def dibujar_peces():
    global lista_peces
    colores = ["#FF6347", "#FFD700", "#FF69B4", "#00CED1", "#FF8C00"]
    for _ in range(5):
        pez = turtle.Turtle()
        pez.shape("triangle")
        pez.color(random.choice(colores))
        pez.shapesize(0.8, 1.5)
        pez.penup()
        pez.goto(random.randint(-400, 400), random.randint(-180, 220))
        pez.setheading(random.choice([0, 180]))
        pez.velocidad_x = random.uniform(0.5, 2) * random.choice([-1, 1])
        lista_peces.append(pez)

def dibujar_burbujas_decorativas():
    global lista_burbujas_deco
    for _ in range(10):
        b = turtle.Turtle()
        b.shape("circle")
        b.color("#FFFFFF")
        b.shapesize(0.4, 0.4)
        b.penup()
        b.goto(random.randint(-400, 400), random.randint(-280, 300))
        b.velocidad_y = random.uniform(0.5, 1.5)
        lista_burbujas_deco.append(b)

def animar_mar():
    if juego_terminado:
        return
    for pez in lista_peces:
        pez.setx(pez.xcor() + pez.velocidad_x)
        if pez.xcor() > 450:
            pez.setx(-450)
        elif pez.xcor() < -450:
            pez.setx(450)
    for burbuja in lista_burbujas_deco:
        burbuja.sety(burbuja.ycor() + burbuja.velocidad_y)
        if burbuja.ycor() > 350:
            burbuja.sety(-300)
            burbuja.setx(random.randint(-400, 400))
    turtle.update()
    turtle.ontimer(animar_mar, 50)

def inicializar_decoraciones():
    dibujar_gradiente()
    dibujar_arena()
    for pos_x in [-380, -280, -100, 50, 200, 340]:
        altura = random.randint(60, 120)
        dibujar_alga(pos_x, altura)
    dibujar_peces()
    dibujar_burbujas_decorativas()
    animar_mar()
