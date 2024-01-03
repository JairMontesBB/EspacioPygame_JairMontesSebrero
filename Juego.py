import pygame
import sys
import random

# Constantes
ANCHO = 1000
ALTO = 700

# Jugador
jugador_size = 50
jugador_pos = [ANCHO / 2, ALTO - jugador_size * 2]

# Enemigo(s)
enemigo_size = 100
enemigo_pos = [random.randint(0, ANCHO - enemigo_size), 0]
enemigo_velocidad = 10
enemigos = []

# Ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Pygame")

# Carga la imagen del espacio como fondo
fondo = pygame.image.load("el_espacio_python_game3.jpg")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Carga la imagen del jugador como jugador
jugador_imagen = pygame.image.load("cohete_python_game.png")
jugador_imagen = pygame.transform.scale(jugador_imagen, (jugador_size, jugador_size))

# Carga la imagen del enemigo como enemigo
enemigo_imagen = pygame.image.load("asteroide_python_game.png")
enemigo_imagen = pygame.transform.scale(enemigo_imagen, (enemigo_size, enemigo_size))

game_over = False
reiniciar = False
clock = pygame.time.Clock()

# Inicializar Pygame
pygame.init()

# Inicializar el temporizador
start_time = pygame.time.get_ticks()
tiempo_ultimo_aumento = pygame.time.get_ticks()

# Funciones
def detectar_colision(jugador_pos, enemigo_pos):
    jx = jugador_pos[0]
    jy = jugador_pos[1]
    ex = enemigo_pos[0]
    ey = enemigo_pos[1]

    porcentaje_interseccion = 0.7  # Ajusta este valor según sea necesario

    # Calcula los límites de intersección
    limite_izquierdo = ex + enemigo_size * (1 - porcentaje_interseccion)
    limite_derecho = ex + enemigo_size * porcentaje_interseccion
    limite_inferior = ey + enemigo_size * (1 - porcentaje_interseccion)
    limite_superior = ey + enemigo_size * porcentaje_interseccion

    # Verifica si más del 30% del cohete toca el asteroide
    if (limite_izquierdo <= jx <= limite_derecho) and (limite_inferior <= jy <= limite_superior):
        return True

    return False

def mostrar_mensaje(tiempo):
    font = pygame.font.Font(None, 48)
    mensaje1 = font.render("Perdiste. Duraste {} segundotes.".format(tiempo), True, (255, 255, 255))
    mensaje2 = font.render("Presiona 'r' para reiniciar.", True, (255, 255, 255))
    ventana.blit(mensaje1, (ANCHO // 2 - 300, ALTO // 2 - 50))
    ventana.blit(mensaje2, (ANCHO // 2 - 300, ALTO // 2 + 10))
    pygame.display.update()

def reiniciar_juego():
    global game_over, jugador_pos, enemigos, enemigo_velocidad, start_time, tiempo_ultimo_aumento
    game_over = False
    jugador_pos[0] = ANCHO / 2
    jugador_pos[1] = ALTO - jugador_size * 2
    enemigos.clear()
    enemigo_velocidad = 10
    start_time = pygame.time.get_ticks()
    tiempo_ultimo_aumento = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reiniciar_juego()

            x = jugador_pos[0]
            if event.key == pygame.K_LEFT:
                x -= jugador_size
            if event.key == pygame.K_RIGHT:
                x += jugador_size

            jugador_pos[0] = x

    # Aumentar la velocidad cada 10 segundos
    current_time = pygame.time.get_ticks()
    if current_time - tiempo_ultimo_aumento > 10000:  # 10000 milisegundos = 10 segundos
        enemigo_velocidad += 1
        tiempo_ultimo_aumento = current_time

    # Dibuja el fondo antes que cualquier otro elemento
    ventana.blit(fondo, (0, 0))

    if not game_over:
        for enemigo in enemigos:
            enemigo[1] += enemigo_velocidad
            ventana.blit(enemigo_imagen, (enemigo[0], enemigo[1]))

            if enemigo[1] > ALTO:
                enemigo[0] = random.randint(0, ANCHO - enemigo_size)
                enemigo[1] = 0

            if detectar_colision(jugador_pos, enemigo):
                game_over = True
                elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
                mostrar_mensaje(elapsed_time)

        ventana.blit(jugador_imagen, (jugador_pos[0], jugador_pos[1]))

        if pygame.key.get_pressed()[pygame.K_r] and game_over:
            reiniciar_juego()

        if random.randint(1, 100) == 1:
            nuevo_enemigo = [random.randint(0, ANCHO - enemigo_size), 0]

            while any(
                (
                    ex - enemigo_size < nuevo_enemigo[0] < ex + enemigo_size
                    or ex - enemigo_size < nuevo_enemigo[0] + enemigo_size < ex + enemigo_size
                )
                and (
                    ey - enemigo_size < nuevo_enemigo[1] < ey + enemigo_size
                    or ey - enemigo_size < nuevo_enemigo[1] + enemigo_size < ey + enemigo_size
                )
                for ex, ey in enemigos
            ):
                nuevo_enemigo = [random.randint(0, ANCHO - enemigo_size), 0]

            enemigos.append(nuevo_enemigo)

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        font = pygame.font.Font(None, 36)
        text = font.render("Tiempo: {} segundos".format(elapsed_time), True, (255, 255, 255))
        ventana.blit(text, (10, 10))

    if game_over:
        mostrar_mensaje(elapsed_time)

    pygame.display.update()
    clock.tick(30)
