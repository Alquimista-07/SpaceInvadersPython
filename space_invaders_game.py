import math
import random

from pygame.locals import *
import pygame
from pygame import mixer

# Inicializar pygame
pygame.init()

# Creamos la pantalla con un tamaño predetermiando
screen = pygame.display.set_mode((800, 600))

# Agregamos el fondo
background = pygame.image.load('resources/background.png')

# Agregamos el sonido
mixer.music.load("resources/background.wav")
mixer.music.play(-1)

# Agregamos el titulo e icono a la ventana
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('resources/ufo.png')
pygame.display.set_icon(icon)

# Agregamos el puntaje con un estilo de texto y un tamanio de letra
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Agregamos el jugador con su posicion
playerImg = pygame.image.load('resources/player.png')
playerX = 370
playerY = 480
playerX_change = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Agregamos los enemigos
# Definimos variables para las posiciones y el numero de enemigos
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Definimos la imagen para los enemigos. Establecemos valores aleatorios para la apricion de los enemigos. Se tiene en cuenta que el rango es menor al tamnio de la pantalla en X y en Y (800, 600) y nos aseguramos que los enemigos no aparezcan en la misma linea del jugador
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('resources/enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Pintar enemigos
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Definimos la funcion para mostrar el puntaje asignando el texto que se va a mostrar y ademas se le asigna el color blanco (255, 255, 255) al texto mostrado
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Bala

# Listo: no puede ver la bala en la pantalla
# Fuego: la bala se está moviendo actualmente

# Asignamos la imagen de la bala, su posición y estado
bulletImg = pygame.image.load('resources/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Funcion para el disparo de las balas
def fire_bullet(x, y):
    # Variables globales
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Funcion de detección colision, encuentra la distancia entre (x1,y1) y (x2,y2)
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

# Funcion para colocacr el fondo
def set_background():
    # Variables globales
    global background
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))

    # Imagen de fondo con su respectiva posicion
    screen.blit(background, (0, 0))

# Funcion para el movimiento de la bala
def move_bullet():
    # Variables globales
    global bulletX, bulletY, bullet_state
    # Movimiento de la bala
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

# Función para las entradas y acciones de teclado en el juego
def game_input():
    # Variables globales
    global running, playerX_change, bulletX, playerX, bulletY
    # Esto sirve para que si por ejemplo se presiona en la X de la ventana esta se cierre y pare la ejecucion de la aplicacion
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Ahora dentro del bucle vamos a capturar los eventos del teclado
        # Si se presiona la tecla, verifique si es derecha, izquierda o tecla espacio
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("resources/laser.wav")
                    bulletSound.play()
                    # Obtiene la coordenada X actual de la nave espacial
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # Detiene el movimiento si se suelta la tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Actualizar la posicion del jugador al mover el jugador y se limita el movimiento al tamanio de la pantalla
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

# Funcion para el movimiento de los enemigos
def enemy_movement():
    # Variables globales
    global enemyX, enemyX_change, enemyY, enemyY_change
    # Movimiento de los enemigos para que los enemigos den la vuelta al movimiento si se cruzan con el borde
    for i in range(num_of_enemies):

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]
 
        # Mostrar enemigos
        enemy(enemyX[i], enemyY[i], i)

# Funcion para las colisiones
def collision():
    # Variales globales
    global num_of_enemies, enemyX, enemyY, bulletX, bulletY, bullet_state, score_value
    for i in range(num_of_enemies):
        # Colision de la bala. Se agrega el sonido de la explosion. Se reinicia la bala. Se incrementa el puntaje y se cambia la posicion del enemigo
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("resources/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)



# Bucle de ejecucion del juego
running = True
while running:
    # Llamamos la funcion para colocar el fondo
    set_background()
    # Llamaos la función para las acciones de teclado del juego
    game_input()
    # Llamamos la funcion del movimiento de los enemigos
    enemy_movement()
    # Llamamos la funcion de colisiones
    collision()
    #Llamamos la función del movimiento de la bala
    move_bullet()
    # Mostramos el jugador en la posicion indicada.  Llamamos dentro del bucle para visualizar cualquier puntaje o texto en la ventana y actualizamos la ventana
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
