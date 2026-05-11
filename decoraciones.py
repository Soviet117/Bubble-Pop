import turtle
import random
import math

ANCHO, ALTO = 900, 650
COLOR_ALGAS       = "#1A5E2A"
COLOR_ALGAS_CLARO = "#52C47A"

lista_peces         = []
lista_burbujas_deco = []
lista_algas         = []
juego_terminado     = False


# ══════════════════════════════════════════════════════════════
#  FONDO OCEÁNICO
# ══════════════════════════════════════════════════════════════

def dibujar_gradiente():
    grad = turtle.Turtle()
    grad.hideturtle(); grad.speed(0); grad.penup()
    pasos = 60
    for i in range(pasos):
        p = i / pasos
        r = int(4  + (10  - 4)  * p)
        g = int(30 + (107 - 30) * p)
        b = int(56 + (140 - 56) * p)
        color   = f"#{r:02x}{g:02x}{b:02x}"
        y_top   = ALTO // 2 - int(i * ALTO / pasos)
        h_franja = math.ceil(ALTO / pasos) + 1
        grad.goto(-ANCHO // 2, y_top)
        grad.pendown(); grad.color(color); grad.begin_fill()
        for _ in range(2):
            grad.forward(ANCHO); grad.right(90)
            grad.forward(h_franja); grad.right(90)
        grad.end_fill(); grad.penup()


def dibujar_manchas_luz():
    for _ in range(10):
        m = turtle.Turtle()
        m.hideturtle(); m.speed(0); m.penup()
        x = random.randint(-350, 350)
        y = random.randint(50, 260)
        for radio, col in [(55, "#1A6B8C"), (38, "#2288A8"),
                           (22, "#3AAAC8"), (10, "#60C8E0")]:
            m.goto(x + random.randint(-5, 5), y + random.randint(-3, 3))
            m.dot(radio, col)


def dibujar_rayos_luz():
    for k in range(5):
        r = turtle.Turtle()
        r.hideturtle(); r.speed(0); r.penup()
        r.goto(-200 + k * 100, 300); r.pendown()
        r.pensize(1); r.color("#1A7A9A")
        r.setheading(random.uniform(-75, -105))
        r.forward(random.randint(120, 200))
        r.penup()


# ══════════════════════════════════════════════════════════════
#  ARENA
# ══════════════════════════════════════════════════════════════

def dibujar_arena():
    t = turtle.Turtle()
    t.hideturtle(); t.speed(0); t.penup()
    for banda in range(8):
        p = banda / 8
        r = int(0xA0 + (0xD4 - 0xA0) * p)
        g = int(0x7B + (0xAA - 0x7B) * p)
        b = int(0x44 + (0x60 - 0x44) * p)
        yb = -250 - banda * 8
        t.goto(-ANCHO // 2, yb); t.pendown()
        t.color(f"#{r:02x}{g:02x}{b:02x}"); t.begin_fill()
        t.goto(ANCHO // 2, yb); t.goto(ANCHO // 2, yb - 9)
        t.goto(-ANCHO // 2, yb - 9); t.end_fill(); t.penup()

    t.goto(-ANCHO // 2, -250); t.pendown()
    t.color("#E8C87A"); t.pensize(2)
    for x in range(-ANCHO // 2, ANCHO // 2, 8):
        t.goto(x, -250 + 5 * math.sin(x * 0.05))
    t.penup()

    for i in range(4):
        yo = -268 + i * 12
        t.goto(-ANCHO // 2, yo); t.pendown()
        t.color("#F5E8C0"); t.pensize(1)
        for x in range(-ANCHO // 2, ANCHO // 2, 6):
            t.goto(x, yo + 3 * math.sin(x * 0.08 + i * 1.2))
        t.penup()

    for _ in range(35):
        t.goto(random.randint(-ANCHO // 2, ANCHO // 2),
               random.randint(-310, -258))
        t.dot(random.randint(2, 5),
              random.choice(["#EEDDAA", "#C8A96E", "#B89050"]))


# ══════════════════════════════════════════════════════════════
#  ALGAS
# ══════════════════════════════════════════════════════════════

def dibujar_alga(x, altura, grosor=3):
    alga = turtle.Turtle()
    alga.hideturtle(); alga.speed(0); alga.penup()
    alga.goto(x, -250); alga.pendown()
    alga.pensize(grosor); alga.color(COLOR_ALGAS)
    for i in range(altura // 5):
        alga.goto(x + 6 * math.sin(i * 0.8), -250 + i * 5)
    alga.color(COLOR_ALGAS_CLARO); alga.pensize(1); alga.penup()
    alga.goto(x, -250); alga.pendown()
    for i in range(altura // 5):
        alga.goto(x - 4 * math.sin(i * 0.7), -250 + i * 5)
    alga.penup()
    for i in range(2, altura // 5, 4):
        lado = 1 if i % 2 == 0 else -1
        alga.goto(x + lado * 8, -250 + i * 5)
        alga.dot(8, "#5ED68A")
    lista_algas.append(alga)


# ══════════════════════════════════════════════════════════════
#  PECES — dibujados con begin_fill, animados con goto
# ══════════════════════════════════════════════════════════════

PALETAS_PEZ = [
    ("#FF7E5A", "#FFBBA0", "#CC4422", "#1A0800"),   # naranja coral
    ("#FFD166", "#FFF0A0", "#CC9900", "#1A1000"),   # amarillo dorado
    ("#06D6A0", "#A0FFE0", "#028860", "#001A10"),   # verde turquesa
    ("#FF69B4", "#FFB8D8", "#CC3380", "#1A0010"),   # rosa
    ("#5BC8FF", "#C0EEFF", "#1A88CC", "#00101A"),   # azul cielo
    ("#FF9F40", "#FFD8A0", "#CC6600", "#1A0800"),   # naranja cálido
]


class Pez:
    """
    Pez compuesto por tortugas con shape="circle"/"triangle" para
    las partes que necesitan moverse fluidamente, y una tortuga
    de dibujo vectorial (begin_fill) para el detalle estático inicial.

    Estrategia de animación:
      - Una tortuga-master "stamp" dibuja el pez completo con begin_fill
        en su posición actual. En cada frame: stamp.clearstamps() y
        se vuelve a dibujar con stamp().
      Esto es más rápido que múltiples begin_fill por frame, porque
      clearstamps() no toca el fondo estático.

    Se usan 4 tortugas stamp (cola, cuerpo, aleta, ojo) para tener
    capas de color sin interferencias.
    """

    def __init__(self, x, y, escala=1.0, hacia_derecha=True):
        self.x   = float(x)
        self.y   = float(y)
        self.esc = escala
        self.dir = hacia_derecha
        self.vx  = (0.6 + random.uniform(0, 0.9)) * (1 if hacia_derecha else -1)
        self.fase = random.uniform(0, math.pi * 2)
        self.tiempo = 0.0
        self.col_cuerpo, self.col_vientre, self.col_acento, self.col_ojo = \
            random.choice(PALETAS_PEZ)

        # Tortuga de dibujo vectorial (invisible, solo pinta)
        self.pincel = turtle.Turtle()
        self.pincel.hideturtle()
        self.pincel.speed(0)
        self.pincel.penup()

        self._dibujar_pez()

    # ─── dibujo vectorial completo ───────────────────────────

    def _dibujar_pez(self):
        """Borra el pez anterior y lo redibuja en self.x, self.y."""
        self.pincel.clear()
        s  = self.esc
        sg = 1 if self.dir else -1
        x, y = self.x, self.y
        p = self.pincel

        # ── cola ─────────────────────────────────────────────
        p.penup()
        p.goto(x - sg * 28 * s, y)
        p.pendown()
        p.color(self.col_acento, self.col_acento)
        p.begin_fill()
        p.goto(x - sg * 48 * s, y + 15 * s)
        p.goto(x - sg * 38 * s, y)
        p.goto(x - sg * 48 * s, y - 15 * s)
        p.goto(x - sg * 28 * s, y)
        p.end_fill()
        p.penup()

        # ── cuerpo (elipse 36 segmentos) ──────────────────────
        p.color(self.col_acento, self.col_cuerpo)
        p.pensize(1)
        p.begin_fill()
        p.goto(x + sg * 22 * s, y)
        for ang in range(0, 361, 10):
            rad = math.radians(ang)
            p.goto(x + sg * 22 * s * math.cos(rad),
                   y  + 11 * s * math.sin(rad))
        p.end_fill()
        p.penup()

        # ── vientre (media elipse inferior, más clara) ─────────
        p.color(self.col_acento, self.col_vientre)
        p.begin_fill()
        p.goto(x - sg * 12 * s, y - 4 * s)
        for ang in range(180, 361, 10):
            rad = math.radians(ang)
            p.goto(x + sg * 12 * s * math.cos(rad),
                   y - 4 * s + 7 * s * math.sin(rad))
        p.end_fill()
        p.penup()

        # ── aleta dorsal ──────────────────────────────────────
        p.color(self.col_acento, self.col_acento)
        p.goto(x - sg * 2 * s, y + 11 * s)
        p.pendown()
        p.begin_fill()
        p.goto(x + sg * 10 * s, y + 24 * s)
        p.goto(x - sg * 10 * s, y + 11 * s)
        p.goto(x - sg * 2  * s, y + 11 * s)
        p.end_fill()
        p.penup()

        # ── aleta pectoral ────────────────────────────────────
        p.color(self.col_acento, self.col_acento)
        p.goto(x + sg * 5 * s, y - 2 * s)
        p.pendown()
        p.begin_fill()
        p.goto(x + sg * 10 * s, y - 14 * s)
        p.goto(x - sg * 2  * s, y - 4  * s)
        p.end_fill()
        p.penup()

        # ── ojo (blanco + pupila) ─────────────────────────────
        ox = x + sg * 15 * s
        oy = y + 3 * s
        p.goto(ox, oy)
        p.dot(int(7 * s), "white")
        p.goto(ox + sg * 0.5 * s, oy)
        p.dot(int(4 * s), self.col_ojo)
        p.goto(ox + sg * 1 * s, oy + 1 * s)
        p.dot(int(2 * s), "white")   # brillo

    # ─── animación ───────────────────────────────────────────

    def actualizar(self):
        self.tiempo += 0.055
        self.x += self.vx
        self.y += math.sin(self.tiempo + self.fase) * 0.45

        # Envolver bordes
        if self.x > ANCHO // 2 + 70:
            self.x = -ANCHO // 2 - 70
        elif self.x < -ANCHO // 2 - 70:
            self.x =  ANCHO // 2 + 70

        self._dibujar_pez()


# ══════════════════════════════════════════════════════════════
#  BURBUJAS DECORATIVAS
# ══════════════════════════════════════════════════════════════

def dibujar_burbujas_decorativas():
    global lista_burbujas_deco
    for _ in range(12):
        b = turtle.Turtle()
        b.shape("circle")
        tam = random.uniform(0.2, 0.55)
        b.shapesize(tam, tam)
        b.color("#B8EEFF", "#B8EEFF")
        b.penup()
        b.goto(random.randint(-400, 400), random.randint(-300, 300))
        b.velocidad_y = random.uniform(0.4, 1.4)
        lista_burbujas_deco.append(b)


# ══════════════════════════════════════════════════════════════
#  BUCLE DE ANIMACIÓN
# ══════════════════════════════════════════════════════════════

def animar_mar():
    if juego_terminado:
        return
    try:
        for pez in lista_peces:
            pez.actualizar()
        for b in lista_burbujas_deco:
            b.sety(b.ycor() + b.velocidad_y)
            if b.ycor() > 340:
                b.sety(-310)
                b.setx(random.randint(-400, 400))
        turtle.update()
        turtle.ontimer(animar_mar, 60)
    except turtle.Terminator:
        pass


# ══════════════════════════════════════════════════════════════
#  INICIALIZACIÓN
# ══════════════════════════════════════════════════════════════

def inicializar_decoraciones():
    dibujar_gradiente()
    dibujar_rayos_luz()
    dibujar_manchas_luz()
    dibujar_arena()

    for pos_x in [-370, -270, -120, 40, 190, 330, 420]:
        dibujar_alga(pos_x, random.randint(70, 130), random.randint(2, 4))

    global lista_peces
    for _ in range(5):
        x   = random.randint(-380, 380)
        y   = random.randint(-190, 200)
        esc = random.uniform(0.75, 1.15)
        der = random.choice([True, False])
        lista_peces.append(Pez(x, y, esc, der))

    dibujar_burbujas_decorativas()
    animar_mar()
