import turtle
import random
import time

ANCHO, ALTO = 900, 650
RADIO_BURBUJA = 55
COLOR_AGUA_SUPERIOR = "#0E5B7A"
COLOR_SELECCION = "#FFD700"
COLOR_VECINO = "#FFA500"
COLOR_TEXTO_NUM = "#003366"
COLOR_BURBUJA_NORMAL = COLOR_AGUA_SUPERIOR

numeros = []
burbujas = []
seleccionada = None
pase_actual = 1
intercambios = 0
juego_terminado = False

sonido_pop = None
sonido_error = None
sonido_victoria = None

info_turtle = None
marcador_turtle = None

# -------------------- BURBUJAS --------------------
def crear_burbuja_juego(x, y, numero, color=COLOR_BURBUJA_NORMAL):
    t_sombra = turtle.Turtle()
    t_sombra.hideturtle()
    t_sombra.penup()
    t_sombra.goto(x + 3, y - 3)
    t_sombra.dot(RADIO_BURBUJA * 2, "#001020")

    t_principal = turtle.Turtle()
    t_principal.hideturtle()
    t_principal.penup()
    t_principal.goto(x, y)
    t_principal.dot(RADIO_BURBUJA * 2, color)

    t_brillo = turtle.Turtle()
    t_brillo.hideturtle()
    t_brillo.penup()
    t_brillo.goto(x - 15, y + 15)
    t_brillo.dot(12, "white")

    t_num = turtle.Turtle()
    t_num.hideturtle()
    t_num.penup()
    t_num.goto(x, y - 12)
    t_num.color(COLOR_TEXTO_NUM)
    t_num.write(numero, align="center", font=("Arial", 26, "bold"))

    return {
        'sombra': t_sombra,
        'principal': t_principal,
        'brillo': t_brillo,
        'texto': t_num,
        'pos': (x, y),
        'valor': numero
    }

def redibujar_burbuja(burbuja, color):
    x, y = burbuja['pos']
    valor = burbuja['valor']
    burbuja['sombra'].clear()
    burbuja['principal'].clear()
    burbuja['brillo'].clear()
    burbuja['texto'].clear()
    burbuja['sombra'].goto(x + 3, y - 3)
    burbuja['sombra'].dot(RADIO_BURBUJA * 2, "#001020")
    burbuja['principal'].goto(x, y)
    burbuja['principal'].dot(RADIO_BURBUJA * 2, color)
    burbuja['brillo'].goto(x - 15, y + 15)
    burbuja['brillo'].dot(12, "white")
    burbuja['texto'].goto(x, y - 12)
    burbuja['texto'].write(valor, align="center", font=("Arial", 26, "bold"))

def crear_burbujas(n=6):
    global numeros, burbujas, info_turtle, marcador_turtle
    numeros = random.sample(range(1, 100), n)
    burbujas = []
    espaciado = 140
    inicio_x = -(n // 2) * espaciado + (espaciado // 2) * (n % 2 == 0)
    for i, num in enumerate(numeros):
        x = inicio_x + i * espaciado
        y = 60
        b = crear_burbuja_juego(x, y, num)
        burbujas.append(b)

    # Panel informativo superior
    panel = turtle.Turtle()
    panel.hideturtle()
    panel.penup()
    panel.goto(-440, 280)
    panel.pendown()
    panel.color("#A0C4E8")
    panel.fillcolor("#A0C4E8")
    panel.begin_fill()
    for _ in range(2):
        panel.forward(880)
        panel.right(90)
        panel.forward(60)
        panel.right(90)
    panel.end_fill()

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
        if indice is not None and i == indice:
            redibujar_burbuja(b, COLOR_SELECCION)
        elif indice is not None and abs(indice - i) == 1:
            redibujar_burbuja(b, COLOR_VECINO)
        else:
            redibujar_burbuja(b, COLOR_BURBUJA_NORMAL)

def mover_burbuja(burbuja, x, y):
    burbuja['principal'].goto(x, y)
    burbuja['sombra'].goto(x + 3, y - 3)
    burbuja['brillo'].goto(x - 15, y + 15)
    burbuja['texto'].goto(x, y - 12)

def intercambiar_burbujas(i, j):
    global numeros, intercambios
    b1, b2 = burbujas[i], burbujas[j]
    x1, y1 = b1['pos']
    x2, y2 = b2['pos']

    # Animación de subida, cruce y bajada
    for paso in range(8):
        mover_burbuja(b1, x1, y1 + paso*8)
        mover_burbuja(b2, x2, y2 + paso*8)
        time.sleep(0.02)
        turtle.update()
    # Cruce horizontal
    mover_burbuja(b1, x2, b1['principal'].ycor())
    mover_burbuja(b2, x1, b2['principal'].ycor())
    for paso in range(8, 0, -1):
        mover_burbuja(b1, x2, y2 + paso*6)
        mover_burbuja(b2, x1, y1 + paso*6)
        time.sleep(0.02)
        turtle.update()

    # Posiciones finales exactas
    mover_burbuja(b1, x2, y2)
    mover_burbuja(b2, x1, y1)

    # Actualizar posiciones en los objetos
    b1['pos'] = (x2, y2)
    b2['pos'] = (x1, y1)

    # Intercambiar los números en la lista global (los valores dentro de las burbujas no cambian)
    numeros[i], numeros[j] = numeros[j], numeros[i]

    # Intercambiar las referencias en la lista para que los índices coincidan con la posición visual
    burbujas[i], burbujas[j] = b2, b1

    # Redibujar todas las burbujas con color normal (se pierde cualquier resaltado)
    for b in burbujas:
        redibujar_burbuja(b, COLOR_BURBUJA_NORMAL)

    intercambios += 1
    actualizar_marcador()
    if sonido_pop:
        sonido_pop.play()

def verificar_ordenado():
    return all(numeros[k] <= numeros[k+1] for k in range(len(numeros)-1))

def finalizar_juego():
    global juego_terminado
    juego_terminado = True
    actualizar_marcador()
    info_turtle.clear()
    info_turtle.goto(0, -240)
    info_turtle.write("🎉 ¡Felicidades! Haz clic para salir.", align="center", font=("Arial", 16, "bold"))
    if sonido_victoria:
        sonido_victoria.play()
    turtle.onscreenclick(lambda x, y: turtle.bye())

def manejar_click(x, y):
    global seleccionada, juego_terminado
    if juego_terminado:
        return
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
                    # Deseleccionar
                    resaltar_vecinos(None)
                    seleccionada = None
                    info_turtle.clear()
                    info_turtle.write("🖱️ Selecciona una burbuja y luego una vecina para intercambiarlas.",
                                      align="center", font=("Arial", 14, "bold"))
                elif abs(seleccionada - i) == 1:
                    if numeros[seleccionada] > numeros[i]:
                        intercambiar_burbujas(seleccionada, i)
                        seleccionada = None
                        # resaltar_vecinos ya se aplicó dentro de intercambiar_burbujas a todos
                        if verificar_ordenado():
                            finalizar_juego()
                        else:
                            info_turtle.clear()
                            info_turtle.write("✅ ¡Intercambio válido! Sigue ordenando.",
                                              align="center", font=("Arial", 14, "bold"))
                    else:
                        if sonido_error:
                            sonido_error.play()
                        t = burbujas[seleccionada]['principal']
                        for _ in range(3):
                            t.setx(t.xcor()+5); time.sleep(0.03)
                            t.setx(t.xcor()-5); time.sleep(0.03)
                            turtle.update()
                        info_turtle.clear()
                        info_turtle.write("❌ No hace falta intercambiar: ya están ordenadas.",
                                          align="center", font=("Arial", 14, "bold"))
                        resaltar_vecinos(None)
                        seleccionada = None
                else:
                    if sonido_error:
                        sonido_error.play()
                    info_turtle.clear()
                    info_turtle.write("❌ Solo puedes intercambiar burbujas vecinas.",
                                      align="center", font=("Arial", 14, "bold"))
                    resaltar_vecinos(None)
                    seleccionada = None
            turtle.update()
            break
    else:
        if seleccionada is not None:
            resaltar_vecinos(None)
            seleccionada = None
            info_turtle.clear()
            info_turtle.write("🖱️ Selecciona una burbuja y luego una vecina para intercambiarlas.",
                              align="center", font=("Arial", 14, "bold"))
            turtle.update()

def inicializar_juego(pop_snd, error_snd, victoria_snd):
    global sonido_pop, sonido_error, sonido_victoria
    sonido_pop = pop_snd
    sonido_error = error_snd
    sonido_victoria = victoria_snd

    crear_burbujas()
    turtle.onscreenclick(manejar_click)
