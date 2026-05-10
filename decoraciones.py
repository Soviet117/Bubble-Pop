import turtle
import random
import math

ANCHO, ALTO = 900, 650
COLOR_ARENA = "#C4974F"
COLOR_ARENA_CLARO = "#D4AA60"
COLOR_ALGAS = "#1A5E2A"
COLOR_ALGAS_CLARO = "#52C47A"

lista_peces = []
lista_burbujas_deco = []
lista_algas = []
juego_terminado = False


# -------------------- FONDO --------------------

def dibujar_gradiente():
    """Gradiente oceánico profundo: azul oscuro arriba, azul-verde abajo."""
    grad = turtle.Turtle()
    grad.hideturtle()
    grad.speed(0)
    grad.penup()

    pasos = 60
    for i in range(pasos):
        proporcion = i / pasos
        # De #041E38 (profundo) a #0A6B8C (medio)
        r = int(4  + (10  - 4)  * proporcion)
        g = int(30 + (107 - 30) * proporcion)
        b = int(56 + (140 - 56) * proporcion)
        color = f"#{r:02x}{g:02x}{b:02x}"
        y_top = ALTO // 2 - int(i * ALTO / pasos)
        altura_franja = math.ceil(ALTO / pasos) + 1
        grad.goto(-ANCHO // 2, y_top)
        grad.pendown()
        grad.color(color)
        grad.begin_fill()
        for _ in range(2):
            grad.forward(ANCHO)
            grad.right(90)
            grad.forward(altura_franja)
            grad.right(90)
        grad.end_fill()
        grad.penup()


def dibujar_manchas_luz():
    """Manchas de luz caustica en el agua (efecto de superficie)."""
    for _ in range(10):
        mancha = turtle.Turtle()
        mancha.hideturtle()
        mancha.speed(0)
        mancha.penup()
        x = random.randint(-350, 350)
        y = random.randint(50, 260)
        mancha.goto(x, y)
        # Elipse aproximada con capas de puntos semitransparentes
        for radio, col in [(55, "#1A6B8C"), (38, "#2288A8"), (22, "#3AAAC8"), (10, "#60C8E0")]:
            ox = random.randint(-6, 6)
            oy = random.randint(-3, 3)
            mancha.goto(x + ox, y + oy)
            mancha.dot(radio, col)


def dibujar_rayos_luz():
    """Rayos diagonales de luz filtrada desde la superficie."""
    for k in range(5):
        rayo = turtle.Turtle()
        rayo.hideturtle()
        rayo.speed(0)
        rayo.penup()
        x_origen = -200 + k * 100
        rayo.goto(x_origen, 300)
        rayo.pendown()
        rayo.pensize(1)
        rayo.color("#1A7A9A")
        largo = random.randint(120, 200)
        angulo = random.uniform(-75, -105)
        rayo.setheading(angulo)
        rayo.forward(largo)
        rayo.penup()


# -------------------- ARENA --------------------

def dibujar_arena():
    arena = turtle.Turtle()
    arena.hideturtle()
    arena.speed(0)
    arena.penup()

    # Cuerpo principal de arena con degradado manual
    for banda in range(8):
        proporcion = banda / 8
        r = int(0xA0 + (0xD4 - 0xA0) * proporcion)
        g = int(0x7B + (0xAA - 0x7B) * proporcion)
        b = int(0x44 + (0x60 - 0x44) * proporcion)
        color = f"#{r:02x}{g:02x}{b:02x}"
        y_base = -250 - banda * 8
        arena.goto(-ANCHO // 2, y_base)
        arena.pendown()
        arena.color(color)
        arena.begin_fill()
        arena.goto(ANCHO // 2, y_base)
        arena.goto(ANCHO // 2, y_base - 9)
        arena.goto(-ANCHO // 2, y_base - 9)
        arena.end_fill()
        arena.penup()

    # Línea ondulada superior de la arena
    arena.goto(-ANCHO // 2, -250)
    arena.pendown()
    arena.color("#E8C87A")
    arena.pensize(2)
    for x in range(-ANCHO // 2, ANCHO // 2, 8):
        arena.goto(x, -250 + 5 * math.sin(x * 0.05))
    arena.penup()

    # Ondas / ripples en la arena
    for i in range(4):
        y_onda = -268 + i * 12
        arena.goto(-ANCHO // 2, y_onda)
        arena.pendown()
        arena.color("#F5E8C0")
        arena.pensize(1)
        for x in range(-ANCHO // 2, ANCHO // 2, 6):
            arena.goto(x, y_onda + 3 * math.sin(x * 0.08 + i * 1.2))
        arena.penup()

    # Pequeñas piedras / puntos decorativos
    for _ in range(35):
        x = random.randint(-ANCHO // 2, ANCHO // 2)
        y = random.randint(-310, -258)
        arena.goto(x, y)
        arena.dot(random.randint(2, 5), random.choice(["#EEDDAA", "#C8A96E", "#B89050"]))

    arena.hideturtle()


# -------------------- ALGAS --------------------

def dibujar_alga(x, altura, grosor=3):
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
        offset_x = 6 * math.sin(i * 0.8)
        alga.goto(x + offset_x, segmento_y)

    # Tallo secundario más claro
    alga.color(COLOR_ALGAS_CLARO)
    alga.pensize(1)
    alga.penup()
    alga.goto(x, -250)
    alga.pendown()
    for i in range(altura // 5):
        segmento_y = -250 + i * 5
        offset_x = -4 * math.sin(i * 0.7)
        alga.goto(x + offset_x, segmento_y)

    # Hojitas laterales
    alga.penup()
    for i in range(2, altura // 5, 4):
        segmento_y = -250 + i * 5
        lado = 1 if i % 2 == 0 else -1
        alga.goto(x + lado * 8, segmento_y)
        alga.dot(8, "#5ED68A")

    lista_algas.append(alga)


# -------------------- PECES --------------------

def dibujar_pez_forma(pez, x, y, color):
    """Dibuja un pez usando stamps con forma de triángulo."""
    pez.shape("triangle")
    pez.color(color)
    pez.shapesize(0.9, 1.6)
    pez.penup()
    pez.goto(x, y)


def dibujar_peces():
    global lista_peces
    colores = ["#FF7E5A", "#FFD166", "#06D6A0", "#FF69B4", "#FF8C00"]
    for _ in range(5):
        pez = turtle.Turtle()
        pez.shape("triangle")
        color = random.choice(colores)
        pez.color(color)
        pez.shapesize(0.9, 1.6)
        pez.penup()
        pez.goto(random.randint(-400, 400), random.randint(-180, 200))
        direccion = random.choice([0, 180])
        pez.setheading(direccion)
        pez.velocidad_x = random.uniform(0.6, 2.0) * (1 if direccion == 0 else -1)
        lista_peces.append(pez)


# -------------------- BURBUJAS DECORATIVAS --------------------

def dibujar_burbujas_decorativas():
    global lista_burbujas_deco
    for _ in range(12):
        b = turtle.Turtle()
        b.shape("circle")
        b.color("#B8EEFF")
        tamanio = random.uniform(0.2, 0.55)
        b.shapesize(tamanio, tamanio)
        b.penup()
        b.goto(random.randint(-400, 400), random.randint(-300, 300))
        b.velocidad_y = random.uniform(0.4, 1.4)
        lista_burbujas_deco.append(b)


# -------------------- ANIMACION --------------------

def animar_mar():
    if juego_terminado:
        return

    for pez in lista_peces:
        pez.setx(pez.xcor() + pez.velocidad_x)
        if pez.xcor() > 460:
            pez.setx(-460)
        elif pez.xcor() < -460:
            pez.setx(460)

    for burbuja in lista_burbujas_deco:
        burbuja.sety(burbuja.ycor() + burbuja.velocidad_y)
        if burbuja.ycor() > 340:
            burbuja.sety(-310)
            burbuja.setx(random.randint(-400, 400))

    turtle.update()
    turtle.ontimer(animar_mar, 50)


# -------------------- INICIALIZACION --------------------

def inicializar_decoraciones():
    dibujar_gradiente()
    dibujar_rayos_luz()
    dibujar_manchas_luz()
    dibujar_arena()

    posiciones_algas = [-370, -270, -120, 40, 190, 330, 420]
    for pos_x in posiciones_algas:
        altura = random.randint(70, 130)
        grosor = random.randint(2, 4)
        dibujar_alga(pos_x, altura, grosor)

    dibujar_peces()
    dibujar_burbujas_decorativas()
    animar_mar()
