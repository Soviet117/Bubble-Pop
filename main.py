import turtle
import os
import pygame
from decoraciones import inicializar_decoraciones, juego_terminado as deco_juego_terminado
from burbujas_juego import inicializar_juego, juego_terminado as juego_juego_terminado

# Configurar ventana
ventana = turtle.Screen()
ventana.title("🐟 Bubble Pop - Ordenamiento Burbuja Submarino")
ventana.bgcolor("#0B3B5C")
ventana.setup(900, 650)
ventana.tracer(0)

# Inicializar pygame mixer
pygame.mixer.init()

RUTA_SONIDOS = os.path.join("assets", "sounds")
def cargar_sonido(nombre):
    ruta = os.path.join(RUTA_SONIDOS, nombre)
    if os.path.exists(ruta):
        return pygame.mixer.Sound(ruta)
    else:
        print(f"⚠️ No se encontró {ruta}")
        return None

sonido_pop = cargar_sonido("pop_correct.wav")
sonido_error = cargar_sonido("wrong.wav")
sonido_victoria = cargar_sonido("victory.wav")

# Música de fondo
fondo = os.path.join(RUTA_SONIDOS, "background.wav")
if os.path.exists(fondo):
    pygame.mixer.music.load(fondo)
    pygame.mixer.music.play(-1)

# Inicializar decoraciones (fondo, algas, peces, burbujitas)
inicializar_decoraciones()

# Inicializar juego (burbujas con números, interacción)
inicializar_juego(sonido_pop, sonido_error, sonido_victoria)

# Mantener la ventana abierta
ventana.mainloop()
