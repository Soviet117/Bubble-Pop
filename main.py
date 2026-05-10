import turtle
import os
import pygame
from game import iniciar_juego

# Configuración de la ventana
ventana = turtle.Screen()
ventana.title("🐟 Bubble Pop - Ordenamiento Burbuja Submarino")
ventana.bgcolor("#0B3B5C")  # Azul marino profundo
ventana.setup(900, 650)
ventana.tracer(0)  # Para animaciones suaves, actualizamos manualmente

# Inicializar pygame mixer para sonido
pygame.mixer.init()

# Rutas de sonido
RUTA_SONIDOS = os.path.join("assets", "sounds")
FONDO = os.path.join(RUTA_SONIDOS, "background.wav")
POP_CORRECTO = os.path.join(RUTA_SONIDOS, "pop_correct.wav")
ERROR = os.path.join(RUTA_SONIDOS, "wrong.wav")
VICTORIA = os.path.join(RUTA_SONIDOS, "victory.wav")

def cargar_sonido(ruta):
    if os.path.exists(ruta):
        return pygame.mixer.Sound(ruta)
    else:
        print(f"⚠️  No se encontró {ruta}, se omitirá el sonido.")
        return None

sonido_pop = cargar_sonido(POP_CORRECTO)
sonido_error = cargar_sonido(ERROR)
sonido_victoria = cargar_sonido(VICTORIA)

# Música de fondo en bucle
if os.path.exists(FONDO):
    pygame.mixer.music.load(FONDO)
    pygame.mixer.music.play(-1)  # Repetir indefinidamente

# Iniciar la lógica del juego
iniciar_juego(ventana, sonido_pop, sonido_error, sonido_victoria)

# Mantener la ventana abierta
ventana.mainloop()
