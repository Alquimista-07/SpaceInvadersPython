import math
import random

import pygame
from pygame import mixer

# Inicializar pygame
pygame.init()

# Creamos la pantalla con un tamaño predetermiando
screen = pygame.display.set_mode((800, 600))

# Agregamos el fondo
background = pygame.image.load('resources/background.png')

# Agregamos el sonido
mixer.music.load('resources/background.wav')
mixer.music.play(-1)

# Agregamos el titulo e icono a la ventana
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('resources/ufo.png')
pygame.display.set_icon(icon)

# Agregamos el jugador
playerImg = pygame.image.load('resources/player.png')
# Aignamos una posicion al jugador
playerX = 370
playerY = 480
playerX_change = 0

# Definimos una funcion para ubicar al jugador dentro de la ventana y pintar el lienzo sobreponiendolo
def player(x, y):
    screen.blit(playerImg, (x, y))

# Bucle de ejecucion del juego
running = True
while running:

    #RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Imagen de fondo con su respectiva posicion
    screen.blit(background, (0, 0))

    # Esto sirve para que si por ejemplo se presiona en la X de la ventana esta se cierre y pare la ejecucion de la aplicacion
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mostramos el jugador en la posicion indicada
    player(playerX, playerY)
    # Actualizamos la ventana
    pygame.display.update()