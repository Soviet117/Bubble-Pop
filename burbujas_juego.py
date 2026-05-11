import turtle
import random
import time
import math

ANCHO, ALTO = 900, 650
RADIO_BURBUJA   = 55          # radio visual en píxeles
SHAPE_SIZE      = 3.67        # RADIO_BURBUJA / 15  (turtle usa unidades de 15px)

COLOR_NORMAL    = "#2FA8D8"
COLOR_SELECCION = "#FFD700"
COLOR_VECINO    = "#FFA500"
COLOR_TEXTO_NUM = "#001830"

numeros         = []
burbujas        = []
seleccionada    = None
pase_actual     = 1
intercambios    = 0
juego_terminado = False

sonido_pop      = None
sonido_error    = None
sonido_victoria = None

info_turtle     = None
marcador_turtle = None


# ══════════════════════════════════════════════════════════════
#  BURBUJA: usa shape="circle" → movible sin tocar el fondo
# ══════════════════════════════════════════════════════════════

def crear_burbuja_juego(x, y, numero, color=COLOR_NORMAL):
    """
    Cada burbuja tiene 3 capas de tortuga con shape circle:
      sombra   → círculo oscuro desplazado
      cuerpo   → círculo de color principal
      brillo   → círculo blanco pequeño arriba-izquierda
    Y una tortuga de texto separada (ésta sí usa write).
    """
    # --- sombra ---
    sombra = turtle.Turtle()
    sombra.hideturtle()
    sombra.shape("circle")
    sombra.shapesize(SHAPE_SIZE * 1.05, SHAPE_SIZE * 1.05)
    sombra.color("#001A2C")
    sombra.penup()
    sombra.goto(x + 5, y - 5)

    # --- cuerpo ---
    cuerpo = turtle.Turtle()
    cuerpo.hideturtle()
    cuerpo.shape("circle")
    cuerpo.shapesize(SHAPE_SIZE, SHAPE_SIZE)
    cuerpo.color("#A8DFFF", color)   # (borde, relleno)
    cuerpo.penup()
    cuerpo.goto(x, y)

    # --- brillo ---
    brillo = turtle.Turtle()
    brillo.hideturtle()
    brillo.shape("circle")
    brillo.shapesize(0.75, 0.75)
    brillo.color("white", "white")
    brillo.penup()
    brillo.goto(x - 16, y + 16)

    # --- número (texto) ---
    texto = turtle.Turtle()
    texto.hideturtle()
    texto.penup()
    texto.color(COLOR_TEXTO_NUM)
    texto.goto(x, y - 13)
    texto.write(numero, align="center", font=("Arial", 24, "bold"))

    b_dict = {
        'sombra':  sombra,
        'cuerpo':  cuerpo,
        'brillo':  brillo,
        'texto':   texto,
        'pos':     (x, y),
        'valor':   numero,
    }
    _mover_conjunto(b_dict, x, y)
    return b_dict


def _mover_conjunto(b, x, y):
    """Mueve las 3 tortugas-shape a la nueva posición (sin redibujar fondo)."""
    b['sombra'].clearstamps()
    b['sombra'].goto(x + 5, y - 5)
    b['sombra'].stamp()
    
    b['cuerpo'].clearstamps()
    b['cuerpo'].goto(x, y)
    b['cuerpo'].stamp()
    
    b['brillo'].clearstamps()
    b['brillo'].goto(x - 16, y + 16)
    b['brillo'].stamp()
    
    # El texto sí hay que borrarlo y reescribirlo
    b['texto'].clear()
    b['texto'].goto(x, y - 13)
    b['texto'].write(b['valor'], align="center", font=("Arial", 24, "bold"))
    b['pos'] = (x, y)


def _set_color_burbuja(b, color):
    b['cuerpo'].fillcolor(color)
    x, y = b['pos']
    _mover_conjunto(b, x, y)


def redibujar_burbuja(b, color):
    _set_color_burbuja(b, color)
    x, y = b['pos']
    _mover_conjunto(b, x, y)   # reescribe el texto en el mismo sitio


def resaltar_vecinos(indice):
    for i, b in enumerate(burbujas):
        if indice is not None and i == indice:
            _set_color_burbuja(b, COLOR_SELECCION)
        elif indice is not None and abs(indice - i) == 1:
            _set_color_burbuja(b, COLOR_VECINO)
        else:
            _set_color_burbuja(b, COLOR_NORMAL)


# ══════════════════════════════════════════════════════════════
#  INICIALIZAR TABLERO
# ══════════════════════════════════════════════════════════════

def crear_burbujas(n=6):
    global numeros, burbujas, info_turtle, marcador_turtle
    numeros   = random.sample(range(1, 100), n)
    burbujas  = []
    espaciado = 140
    inicio_x  = -(n // 2) * espaciado + (espaciado // 2) * (n % 2 == 0)

    for i, num in enumerate(numeros):
        x = inicio_x + i * espaciado
        burbujas.append(crear_burbuja_juego(x, 60, num))

    # Panel informativo superior
    panel = turtle.Turtle()
    panel.hideturtle(); panel.penup()
    panel.goto(-440, 280); panel.pendown()
    panel.color("#7ABEDC"); panel.fillcolor("#0D4F6E")
    panel.begin_fill()
    for _ in range(2):
        panel.forward(880); panel.right(90)
        panel.forward(58);  panel.right(90)
    panel.end_fill()

    info_turtle = turtle.Turtle()
    info_turtle.hideturtle(); info_turtle.penup()
    info_turtle.goto(0, -240); info_turtle.color("white")
    info_turtle.write(
        "🖱 Selecciona una burbuja y luego una vecina para ordenar.",
        align="center", font=("Arial", 14, "bold")
    )

    marcador_turtle = turtle.Turtle()
    marcador_turtle.hideturtle(); marcador_turtle.penup()
    marcador_turtle.goto(0, 309); marcador_turtle.color("white")
    actualizar_marcador()


def actualizar_marcador():
    marcador_turtle.clear()
    marcador_turtle.write(
        f"🌀 Pase: {pase_actual}  |  💱 Intercambios: {intercambios}",
        align="center", font=("Arial", 18, "bold")
    )
    if juego_terminado:
        marcador_turtle.goto(0, 280)
        marcador_turtle.write(
            "¡LISTA ORDENADA! 🎉", align="center", font=("Arial", 22, "bold")
        )


# ══════════════════════════════════════════════════════════════
#  ANIMACIÓN DE INTERCAMBIO
#  Las tortugas-shape se mueven con .goto() → sin parpadeo,
#  sin tocar el fondo. Solo el texto usa .clear() + write.
# ══════════════════════════════════════════════════════════════

def intercambiar_burbujas(i, j):
    global numeros, intercambios

    b1, b2 = burbujas[i], burbujas[j]
    x1, y1 = b1['pos']
    x2, y2 = b2['pos']

    PASOS = 45
    ARCO  = 105   # altura máxima del arco en píxeles

    _set_color_burbuja(b1, COLOR_SELECCION)   # dorado: pasa por arriba
    _set_color_burbuja(b2, COLOR_VECINO)       # naranja: pasa por abajo

    for paso in range(PASOS + 1):
        p    = paso / PASOS
        t    = p * p * (3.0 - 2.0 * p)        # smoothstep
        elev = math.sin(p * math.pi)           # arco simétrico

        nx1 = x1 + t * (x2 - x1)
        ny1 = y1 + elev * ARCO                 # sube alto

        nx2 = x2 + t * (x1 - x2)
        ny2 = y2 + elev * ARCO * 0.40          # sube menos → cruza por debajo

        _mover_conjunto(b1, nx1, ny1)
        _mover_conjunto(b2, nx2, ny2)
        turtle.update()
        time.sleep(0.011)

    # Posiciones finales exactas
    _mover_conjunto(b1, x2, y2)
    _mover_conjunto(b2, x1, y1)
    b1['pos'] = (x2, y2)
    b2['pos'] = (x1, y1)

    numeros[i],  numeros[j]  = numeros[j],  numeros[i]
    burbujas[i], burbujas[j] = b2, b1

    for b in burbujas:
        _set_color_burbuja(b, COLOR_NORMAL)

    intercambios += 1
    actualizar_marcador()
    if sonido_pop:
        sonido_pop.play()


# ══════════════════════════════════════════════════════════════
#  LÓGICA DE JUEGO
# ══════════════════════════════════════════════════════════════

def verificar_ordenado():
    return all(numeros[k] <= numeros[k + 1] for k in range(len(numeros) - 1))


def finalizar_juego():
    global juego_terminado
    juego_terminado = True
    actualizar_marcador()
    info_turtle.clear()
    info_turtle.goto(0, -240)
    info_turtle.write(
        "🎉 ¡Felicidades! Haz clic para salir.",
        align="center", font=("Arial", 16, "bold")
    )
    if sonido_victoria:
        sonido_victoria.play()
    turtle.onscreenclick(lambda x, y: turtle.bye())


def manejar_click(x, y):
    global seleccionada, juego_terminado
    if juego_terminado:
        return

    for i, b in enumerate(burbujas):
        bx, by = b['pos']
        if math.hypot(x - bx, y - by) <= RADIO_BURBUJA:

            if seleccionada is None:
                seleccionada = i
                resaltar_vecinos(i)
                info_turtle.clear()
                info_turtle.write(
                    "👉 Haz clic en una burbuja naranja (vecina) para intercambiar.",
                    align="center", font=("Arial", 14, "bold")
                )

            else:
                if seleccionada == i:
                    resaltar_vecinos(None)
                    seleccionada = None
                    info_turtle.clear()
                    info_turtle.write(
                        "🖱 Selecciona una burbuja y luego una vecina.",
                        align="center", font=("Arial", 14, "bold")
                    )

                elif abs(seleccionada - i) == 1:
                    izq = min(seleccionada, i)
                    der = max(seleccionada, i)

                    if numeros[izq] > numeros[der]:
                        intercambiar_burbujas(izq, der)
                        seleccionada = None
                        if verificar_ordenado():
                            finalizar_juego()
                        else:
                            info_turtle.clear()
                            info_turtle.write(
                                "✅ ¡Intercambio válido! Sigue ordenando.",
                                align="center", font=("Arial", 14, "bold")
                            )
                    else:
                        if sonido_error:
                            sonido_error.play()
                        # Vibración de error sin borrar fondo
                        bx0, by0 = burbujas[seleccionada]['pos']
                        for _ in range(4):
                            _mover_conjunto(burbujas[seleccionada], bx0 + 7, by0)
                            turtle.update(); time.sleep(0.03)
                            _mover_conjunto(burbujas[seleccionada], bx0 - 7, by0)
                            turtle.update(); time.sleep(0.03)
                        _mover_conjunto(burbujas[seleccionada], bx0, by0)
                        turtle.update()
                        info_turtle.clear()
                        info_turtle.write(
                            "❌ Ya están ordenadas, no hace falta intercambiar.",
                            align="center", font=("Arial", 14, "bold")
                        )
                        resaltar_vecinos(None)
                        seleccionada = None

                else:
                    if sonido_error:
                        sonido_error.play()
                    info_turtle.clear()
                    info_turtle.write(
                        "❌ Solo puedes intercambiar burbujas vecinas.",
                        align="center", font=("Arial", 14, "bold")
                    )
                    resaltar_vecinos(None)
                    seleccionada = None

            turtle.update()
            return

    # Clic en zona vacía
    if seleccionada is not None:
        resaltar_vecinos(None)
        seleccionada = None
        info_turtle.clear()
        info_turtle.write(
            "🖱 Selecciona una burbuja y luego una vecina.",
            align="center", font=("Arial", 14, "bold")
        )
        turtle.update()


def inicializar_juego(pop_snd, error_snd, victoria_snd):
    global sonido_pop, sonido_error, sonido_victoria
    sonido_pop      = pop_snd
    sonido_error    = error_snd
    sonido_victoria = victoria_snd
    crear_burbujas()
    turtle.onscreenclick(manejar_click)
