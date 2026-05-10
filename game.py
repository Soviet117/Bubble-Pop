import turtle
import random
import time
import math

# -------------------- CONFIGURACIÓN GLOBAL --------------------
ANCHO, ALTO = 900, 650
RADIO_BURBUJA = 55
COLOR_AGUA_SUPERIOR = "#0E5B7A"
COLOR_AGUA_INFERIOR = "#021B2B"
COLOR_ARENA = "#D2B48C"
COLOR_ALGAS = "#2E8B57"
COLOR_ALGAS_CLARO = "#3CB371"
COLOR_SELECCION = "#FFD700"
COLOR_VECINO = "#FFA500"
COLOR_TEXTO = "white"
COLOR_TEXTO_NUM = "#003366"

# Estado del juego
numeros = []
burbujas = []
seleccionada = None
pase_actual = 1
intercambios = 0
juego_terminado = False
sonido_pop = None
sonido_error = None
sonido_victoria = None

# Elementos gráficos
info_turtle = None
marcador_turtle = None
elementos_decorativos = []  # peces, algas, burbujas decorativas

# -------------------- DIBUJO DEL FONDO --------------------
def dibujar_gradiente():
    """Simula un degradado marino con rectángulos de color."""
    grad = turtle.Turtle()
    grad.hideturtle()
    grad.speed(0)
    grad.penup()
    pasos = 50
    for i in range(pasos):
        proporcion = i / pasos
        r1, g1, b1 = int(0x02 + (0x0E-0x02)*proporcion), int(0x1B + (0x5B-0x1B)*proporcion), int(0x2B + (0x7A-0x2B)*proporcion)
        color = f"#{r1:02x}{g1:02x}{b1:02x}"
        grad.goto(-ANCHO//2, ALTO//2 - (i * ALTO/pasos))
        grad.pendown()
        grad.color(color)
        grad.begin_fill()
        grad.goto(ANCHO//2, ALTO//2 - (i * ALTO/pasos))
        grad.goto(ANCHO//2, ALTO//2 - ((i+1) * ALTO/pasos))
        grad.goto(-ANCHO//2, ALTO//2 - ((i+1) * ALTO/pasos))
        grad.end_fill()
    grad.hideturtle()

def dibujar_arena():
    """Arena con pequeñas ondulaciones y puntos de arena suspendida."""
    arena = turtle.Turtle()
    arena.hideturtle()
    arena.speed(0)
    arena.penup()
    # Arena base
    arena.goto(-ANCHO//2, -250)
    arena.color(COLOR_ARENA)
    arena.begin_fill()
    arena.goto(ANCHO//2, -250)
    arena.goto(ANCHO//2, -ALTO//2)
    arena.goto(-ANCHO//2, -ALTO//2)
    arena.end_fill()
    # Ondulación simple en la superficie de la arena
    arena.goto(-ANCHO//2, -250)
    arena.color("#F5DEB3")
    arena.pensize(3)
    for x in range(-ANCHO//2, ANCHO//2, 10):
        arena.goto(x, -250 + 5 * math.sin(x * 0.05))
    # Puntos decorativos sobre la arena
    for _ in range(30):
        x = random.randint(-ANCHO//2, ANCHO//2)
        y = random.randint(-280, -255)
        arena.goto(x, y)
        arena.dot(3, "#EEDDAA")

def dibujar_alga(x, altura, grosor=2):
    """Dibuja un alga en posición x, con altura y retorna los turtles creados."""
    alga = turtle.Turtle()
    alga.hideturtle()
    alga.speed(0)
    alga.penup()
    alga.goto(x, -250)
    alga.pendown()
    alga.pensize(grosor)
    alga.color(COLOR_ALGAS)
    # Forma ondulada: sube y se curva
    for i in range(altura // 5):
        segmento_y = -250 + i * 5
        offset_x = 5 * math.sin(i * 0.8)  # ondulación natural
        alga.goto(x + offset_x, segmento_y)
    # Segundo tallo más fino
    alga.color(COLOR_ALGAS_CLARO)
    alga.pensize(1)
    alga.penup()
    alga.goto(x, -250)
    alga.pendown()
    for i in range(altura // 5):
        segmento_y = -250 + i * 5
        offset_x = -3 * math.sin(i * 0.7)
        alga.goto(x + offset_x, segmento_y)
    return alga

def dibujar_peces():
    """Crea varios pececillos que nadarán horizontalmente."""
    peces = []
    for _ in range(5):
        pez = turtle.Turtle()
        pez.shape("triangle")
        pez.color(random.choice(["#FF6347", "#FFD700", "#FF69B4", "#00CED1"]))
        pez.shapesize(0.8, 1.5)
        pez.penup()
        pez.goto(random.randint(-400, 400), random.randint(-200, 200))
        pez.setheading(random.choice([0, 180]))  # mirar izquierda o derecha
        pez.velocidad_x = random.uniform(0.5, 2) * random.choice([-1, 1])
        peces.append(pez)
    return peces

def dibujar_burbujas_decorativas():
    """Crea burbujitas flotantes como decoración."""
    burbujas_deco = []
    for _ in range(10):
        b = turtle.Turtle()
        b.shape("circle")
        b.color("#FFFFFF")
        b.shapesize(0.4, 0.4)
        b.penup()
        b.goto(random.randint(-400, 400), random.randint(-280, 300))
        b.velocidad_y = random.uniform(0.5, 1.5)
        burbujas_deco.append(b)
    return burbujas_deco

# -------------------- ANIMACIÓN CONTINUA --------------------
def animar_mar():
    """Hace que las algas se balanceen y las burbujitas suban."""
    if juego_terminado:
        return
    # Separamos las listas de peces y burbujas de los elementos individuales (algas)
    listas = [elem for elem in elementos_decorativos if isinstance(elem, list)]
    lista_peces = listas[0] if len(listas) > 0 else []
    lista_burbujas = listas[1] if len(listas) > 1 else []

    # Movimiento de peces
    for pez in lista_peces:
        pez.setx(pez.xcor() + pez.velocidad_x)
        if pez.xcor() > 450:
            pez.setx(-450)
        elif pez.xcor() < -450:
            pez.setx(450)
    # Subida de burbujas decorativas
    for burbuja in lista_burbujas:
        burbuja.sety(burbuja.ycor() + burbuja.velocidad_y)
        if burbuja.ycor() > 350:
            burbuja.sety(-300)
            burbuja.setx(random.randint(-400, 400))
    turtle.update()
    turtle.ontimer(animar_mar, 50)  # ~20 fps

# -------------------- BURBUJAS DEL JUEGO --------------------
def crear_burbuja_juego(x, y, numero, color=COLOR_AGUA_SUPERIOR):
    """Crea un grupo de turtles para una burbuja con número, brillo y sombra."""
    t_sombra = turtle.Turtle()
    t_sombra.hideturtle()
    t_sombra.penup()
    # Sombra ligeramente desplazada
    t_sombra.goto(x + 3, y - 3)
    t_sombra.dot(RADIO_BURBUJA * 2, "gray")  # color con opacidad no funciona en Turtle, usamos gris
    t_sombra.dot(RADIO_BURBUJA * 2, "#002233")

    t_principal = turtle.Turtle()
    t_principal.hideturtle()
    t_principal.penup()
    t_principal.goto(x, y)
    t_principal.dot(RADIO_BURBUJA * 2, color)

    # Brillo (círculo blanco pequeño arriba a la izquierda)
    t_brillo = turtle.Turtle()
    t_brillo.hideturtle()
    t_brillo.penup()
    t_brillo.goto(x - 15, y + 15)
    t_brillo.dot(12, "white")

    # Número
    t_num = turtle.Turtle()
    t_num.hideturtle()
    t_num.penup()
    t_num.goto(x, y - 12)
    t_num.color(COLOR_TEXTO_NUM)
    t_num.write(numero, align="center", font=("Arial", 26, "bold"))

    return {'sombra': t_sombra, 'principal': t_principal, 'brillo': t_brillo, 'texto': t_num, 'pos': (x, y)}

def redibujar_burbuja_juego(burbuja_dict, color):
    """Redibuja una burbuja cambiando su color y manteniendo el número."""
    x, y = burbuja_dict['pos']
    valor = burbuja_dict['texto'].value  # no hay atributo value directo, lo guardaremos aparte
    # Limpiamos todo
    burbuja_dict['principal'].clear()
    burbuja_dict['brillo'].clear()
    burbuja_dict['texto'].clear()
    # Redibujar
    burbuja_dict['principal'].goto(x, y)
    burbuja_dict['principal'].dot(RADIO_BURBUJA * 2, color)
    burbuja_dict['brillo'].goto(x - 15, y + 15)
    burbuja_dict['brillo'].dot(12, "white")
    burbuja_dict['texto'].goto(x, y - 12)
    burbuja_dict['texto'].write(valor, align="center", font=("Arial", 26, "bold"))

def crear_burbujas(n=6):
    global numeros, burbujas
    numeros = random.sample(range(1, 100), n)
    burbujas = []
    espaciado = 140
    inicio_x = -(n // 2) * espaciado + (espaciado // 2) * (n % 2 == 0)
    for i, num in enumerate(numeros):
        x = inicio_x + i * espaciado
        y = 60
        b = crear_burbuja_juego(x, y, num)
        b['valor'] = num  # guardamos el número para acceso rápido
        burbujas.append(b)

    # Panel de información
    global info_turtle, marcador_turtle
    # Rectángulo semitransparente simulado (simple rectángulo blanco muy claro)
    panel = turtle.Turtle()
    panel.hideturtle()
    panel.penup()
    panel.goto(-440, 280)
    panel.pendown()
    panel.color("lightgray")  # Esto no funciona, usaremos un gris claro
    panel.fillcolor("#A0C4E8")
    panel.begin_fill()
    for _ in range(2):
        panel.forward(880)
        panel.right(90)
        panel.forward(60)
        panel.right(90)
    panel.end_fill()
    panel.hideturtle()

    info_turtle = turtle.Turtle()
    info_turtle.hideturtle()
    info_turtle.penup()
    info_turtle.goto(0, -240)
    info_turtle.color("white")
    info_turtle.write("🖱️ Selecciona una burbuja y luego una vecina para ordenar.",
                      align="center", font=("Arial", 14, "bold"))

    marcador_turtle = turtle.Turtle()
    marcador_turtle.hideturtle()
    marcador_turtle.penup()
    marcador_turtle.goto(0, 310)
    marcador_turtle.color("white")
    actualizar_marcador()

def actualizar_marcador():
    marcador_turtle.clear()
    marcador_turtle.write(f"🌀 Pase: {pase_actual}  |  💱 Intercambios: {intercambios}",
                          align="center", font=("Arial", 18, "bold"))
    if juego_terminado:
        marcador_turtle.goto(0, 280)
        marcador_turtle.write("¡LISTA ORDENADA! 🎉", align="center", font=("Arial", 22, "bold"))

def resaltar_vecinos(indice):
    for i, b in enumerate(burbujas):
        if i == indice:
            redibujar_burbuja_juego(b, COLOR_SELECCION)
        elif abs(indice - i) == 1:
            redibujar_burbuja_juego(b, COLOR_VECINO)
        else:
            redibujar_burbuja_juego(b, COLOR_AGUA_SUPERIOR)

def intercambiar_burbujas(i, j):
    global numeros, intercambios
    b1, b2 = burbujas[i], burbujas[j]
    x1, y1 = b1['pos']
    x2, y2 = b2['pos']
    # Animación: subir, cruzar, bajar.
    for paso in range(8):
        b1['principal'].sety(y1 + paso*8)
        b1['brillo'].sety(y1 + 15 + paso*8)
        b1['texto'].sety(y1 - 12 + paso*8)
        b2['principal'].sety(y2 + paso*8)
        b2['brillo'].sety(y2 + 15 + paso*8)
        b2['texto'].sety(y2 - 12 + paso*8)
        time.sleep(0.02); turtle.update()
    # Cruzar
    b1['principal'].goto(x2, b1['principal'].ycor())
    b1['brillo'].goto(x2 - 15, b1['brillo'].ycor())
    b1['texto'].goto(x2, b1['texto'].ycor())
    b2['principal'].goto(x1, b2['principal'].ycor())
    b2['brillo'].goto(x1 - 15, b2['brillo'].ycor())
    b2['texto'].goto(x1, b2['texto'].ycor())
    # Bajar
    for paso in range(8, 0, -1):
        b1['principal'].sety(y2 + paso*6)
        b1['brillo'].sety(y2 + 15 + paso*6)
        b1['texto'].sety(y2 - 12 + paso*6)
        b2['principal'].sety(y1 + paso*6)
        b2['brillo'].sety(y1 + 15 + paso*6)
        b2['texto'].sety(y1 - 12 + paso*6)
        time.sleep(0.02); turtle.update()
    # Actualizar posiciones
    b1['pos'] = (x2, y2)
    b2['pos'] = (x1, y1)
    numeros[i], numeros[j] = numeros[j], numeros[i]
    burbujas[i], burbujas[j] = burbujas[j], burbujas[i]
    intercambios += 1
    actualizar_marcador()
    if sonido_pop: sonido_pop.play()

def verificar_ordenado():
    return all(numeros[k] <= numeros[k+1] for k in range(len(numeros)-1))

def finalizar_juego():
    global juego_terminado
    juego_terminado = True
    actualizar_marcador()
    info_turtle.clear()
    info_turtle.goto(0, -240)
    info_turtle.write("🎉 ¡Felicidades! Haz clic para salir.", align="center", font=("Arial", 16, "bold"))
    if sonido_victoria: sonido_victoria.play()
    turtle.onscreenclick(lambda x,y: turtle.bye())

def manejar_click(x, y):
    global seleccionada, juego_terminado
    if juego_terminado: return
    for i, b in enumerate(burbujas):
        bx, by = b['pos']
        if (bx - RADIO_BURBUJA <= x <= bx + RADIO_BURBUJA and
            by - RADIO_BURBUJA <= y <= by + RADIO_BURBUJA):
            if seleccionada is None:
                seleccionada = i
                resaltar_vecinos(i)
                info_turtle.clear()
                info_turtle.write("👉 Ahora haz clic en una burbuja naranja (vecina) para intercambiar.",
                                  align="center", font=("Arial", 14, "bold"))
            else:
                if seleccionada == i:
                    resaltar_vecinos(-1)
                    seleccionada = None
                    info_turtle.clear()
                    info_turtle.write("🖱️ Selecciona una burbuja y luego una vecina para intercambiarlas.",
                                      align="center", font=("Arial", 14, "bold"))
                elif abs(seleccionada - i) == 1:
                    if numeros[seleccionada] > numeros[i]:
                        intercambiar_burbujas(seleccionada, i)
                        seleccionada = None
                        if verificar_ordenado():
                            finalizar_juego()
                        else:
                            info_turtle.clear()
                            info_turtle.write("✅ ¡Intercambio válido! Sigue ordenando.",
                                              align="center", font=("Arial", 14, "bold"))
                    else:
                        if sonido_error: sonido_error.play()
                        t = burbujas[seleccionada]['principal']
                        for _ in range(3):
                            t.setx(t.xcor()+5); time.sleep(0.03)
                            t.setx(t.xcor()-5); time.sleep(0.03); turtle.update()
                        info_turtle.clear()
                        info_turtle.write("❌ No hace falta intercambiar: ya están ordenadas.",
                                          align="center", font=("Arial", 14, "bold"))
                        resaltar_vecinos(-1)
                        seleccionada = None
                else:
                    if sonido_error: sonido_error.play()
                    info_turtle.clear()
                    info_turtle.write("❌ Solo puedes intercambiar burbujas vecinas.",
                                      align="center", font=("Arial", 14, "bold"))
                    resaltar_vecinos(-1)
                    seleccionada = None
            turtle.update()
            break
    else:
        if seleccionada is not None:
            resaltar_vecinos(-1)
            seleccionada = None
            info_turtle.clear()
            info_turtle.write("🖱️ Selecciona una burbuja y luego una vecina para intercambiarlas.",
                              align="center", font=("Arial", 14, "bold"))
            turtle.update()

def iniciar_juego(ventana, pop_snd, error_snd, victoria_snd):
    global sonido_pop, sonido_error, sonido_victoria
    sonido_pop, sonido_error, sonido_victoria = pop_snd, error_snd, victoria_snd

    dibujar_gradiente()
    dibujar_arena()
    # Algas (variables según altura)
    for pos_x in [-380, -280, -100, 50, 200, 340]:
        altura = random.randint(60, 120)
        alga = dibujar_alga(pos_x, altura)
        elementos_decorativos.append(alga)
    # Peces
    peces = dibujar_peces()
    burbujas_deco = dibujar_burbujas_decorativas()
    elementos_decorativos.append(peces)
    elementos_decorativos.append(burbujas_deco)

    crear_burbujas()
    turtle.onscreenclick(manejar_click)
    animar_mar()  # inicia el loop de animación
    turtle.update()
