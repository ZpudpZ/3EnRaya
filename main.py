import pygame
import sys

# Inicializar pygame
pygame.init()

# Definir colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
COLOR_LINEA = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)

# Tamaño de la pantalla
ANCHO = 600
ALTO = 600
GROSOR_LINEA = 15

# Definir el tamaño del tablero
FILAS_TABLERO = 3
COLUMNAS_TABLERO = 3
TAMANIO_CUADRADO = ANCHO // COLUMNAS_TABLERO

# Cargar la fuente para el texto
FUENTE = pygame.font.Font(None, 100)
FUENTE_MENU = pygame.font.Font(None, 60)

# Definir jugadores
X = "X"
O = "O"
VACIO = None

# Crear la ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption('Tres en Raya')

# Dibujar las líneas del tablero
def draw_lines():
    pantalla.fill(BLANCO)
    # Líneas horizontales
    pygame.draw.line(pantalla, COLOR_LINEA, (0, TAMANIO_CUADRADO), (ANCHO, TAMANIO_CUADRADO), GROSOR_LINEA)
    pygame.draw.line(pantalla, COLOR_LINEA, (0, 2 * TAMANIO_CUADRADO), (ANCHO, 2 * TAMANIO_CUADRADO), GROSOR_LINEA)
    # Líneas verticales
    pygame.draw.line(pantalla, COLOR_LINEA, (TAMANIO_CUADRADO, 0), (TAMANIO_CUADRADO, ALTO), GROSOR_LINEA)
    pygame.draw.line(pantalla, COLOR_LINEA, (2 * TAMANIO_CUADRADO, 0), (2 * TAMANIO_CUADRADO, ALTO), GROSOR_LINEA)

# Dibujar X y O
# Dibujar X y O
def draw_figures(board):
    for fila in range(FILAS_TABLERO):
        for col in range(COLUMNAS_TABLERO):
            if board[fila][col] == X:
                texto = FUENTE.render(X, True, ROJO)
                # Centrar la X
                pantalla.blit(texto, (col * TAMANIO_CUADRADO + (TAMANIO_CUADRADO - texto.get_width()) // 2,
                                       fila * TAMANIO_CUADRADO + (TAMANIO_CUADRADO - texto.get_height()) // 2))
            elif board[fila][col] == O:
                texto = FUENTE.render(O, True, VERDE)
                # Centrar la O
                pantalla.blit(texto, (col * TAMANIO_CUADRADO + (TAMANIO_CUADRADO - texto.get_width()) // 2,
                                       fila * TAMANIO_CUADRADO + (TAMANIO_CUADRADO - texto.get_height()) // 2))

# Pantalla de inicio para seleccionar el modo de juego
def pantalla_inicio():
    pantalla.fill(BLANCO)
    texto_menu = FUENTE_MENU.render("Tres en Raya", True, NEGRO)
    pantalla.blit(texto_menu, (ANCHO // 4, ALTO // 5))

    texto_op1 = FUENTE_MENU.render("1. Jugador vs IA", True, NEGRO)
    pantalla.blit(texto_op1, (ANCHO // 6, ALTO // 2))

    texto_op2 = FUENTE_MENU.render("2. Jugador vs Jugador", True, NEGRO)
    pantalla.blit(texto_op2, (ANCHO // 6, ALTO // 1.7))

    texto_op3 = FUENTE_MENU.render("3. Salir", True, NEGRO)
    pantalla.blit(texto_op3, (ANCHO // 6, ALTO // 1.5))

    pygame.display.update()

# Mostrar el resultado al final del juego
def mostrar_resultado(resultado):
    pantalla.fill(BLANCO, (0, ALTO - 60, ANCHO, 60))  # Borrar área de texto
    texto_resultado = FUENTE_MENU.render(resultado, True, NEGRO)
    pantalla.blit(texto_resultado, (ANCHO // 4, ALTO - 60))
    pygame.display.update()

# Mostrar el botón de "Volver al Menú"
def mostrar_boton_menu():
    texto_menu = FUENTE_MENU.render("M para volver al Menu", True, NEGRO)
    # Ajustar posición para que esté visible
    pantalla.blit(texto_menu, (ANCHO // 10, ALTO - 150))  # Cambia la posición Y a -150
    pygame.display.update()


# Reiniciar el tablero
def reiniciar_tablero():
    return [[VACIO] * COLUMNAS_TABLERO for _ in range(FILAS_TABLERO)]

# Verificar si el estado es terminal (victoria o empate)
def terminal(board):
    for i in range(FILAS_TABLERO):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not VACIO:
            return True
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not VACIO:
            return True
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not VACIO:
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not VACIO:
        return True
    return all(all(celda is not VACIO for celda in fila) for fila in board)

# Evaluar el estado del tablero
def utility(board):
    for i in range(FILAS_TABLERO):
        if board[i][0] == board[i][1] == board[i][2]:
            if board[i][0] == X:
                return 1
            elif board[i][0] == O:
                return -1
        if board[0][i] == board[1][i] == board[2][i]:
            if board[0][i] == X:
                return 1
            elif board[0][i] == O:
                return -1
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] == X:
            return 1
        elif board[0][0] == O:
            return -1
    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] == X:
            return 1
        elif board[0][2] == O:
            return -1
    return 0

# Ejecutar el movimiento y devolver el nuevo estado
def result(board, action, player):
    nuevo_tablero = [fila.copy() for fila in board]
    i, j = action
    nuevo_tablero[i][j] = player
    return nuevo_tablero

# Función para determinar el mejor movimiento de la IA usando Minimax
def minimax(tablero, jugador):
    if terminal(tablero):
        return utility(tablero), None

    if jugador == X:  # Maximizador
        mejor_valor = -float('inf')
        mejor_movimiento = None
        for i in range(FILAS_TABLERO):
            for j in range(COLUMNAS_TABLERO):
                if tablero[i][j] is VACIO:
                    valor, _ = minimax(result(tablero, (i, j), X), O)
                    if valor > mejor_valor:
                        mejor_valor = valor
                        mejor_movimiento = (i, j)
        return mejor_valor, mejor_movimiento
    else:  # Minimizar
        mejor_valor = float('inf')
        mejor_movimiento = None
        for i in range(FILAS_TABLERO):
            for j in range(COLUMNAS_TABLERO):
                if tablero[i][j] is VACIO:
                    valor, _ = minimax(result(tablero, (i, j), O), X)
                    if valor < mejor_valor:
                        mejor_valor = valor
                        mejor_movimiento = (i, j)
        return mejor_valor, mejor_movimiento

# IA elige el mejor movimiento
def mejor_movimiento_IA(tablero):
    _, movimiento = minimax(tablero, O)
    return movimiento

# Función principal para el juego
# Cargar los sonidos
sonido_clic = pygame.mixer.Sound("clic.wav")
sonido_ganar = pygame.mixer.Sound("ganar.wav")

# Función principal para el juego
def main():
    global tablero, jugador, juego_terminado
    tablero = reiniciar_tablero()
    jugador = X
    juego_terminado = False
    modo_juego = None

    pantalla_inicio()
    esperando_menu = True

    while esperando_menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    modo_juego = "IA"
                    esperando_menu = False
                elif evento.key == pygame.K_2:
                    modo_juego = "jugador"
                    esperando_menu = False
                elif evento.key == pygame.K_3:
                    pygame.quit()
                    sys.exit()

    pantalla.fill(BLANCO)
    draw_lines()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_m:
                    main()

            if evento.type == pygame.MOUSEBUTTONDOWN and not juego_terminado:
                mouse_x, mouse_y = evento.pos
                clicked_row = mouse_y // TAMANIO_CUADRADO
                clicked_col = mouse_x // TAMANIO_CUADRADO

                if tablero[clicked_row][clicked_col] is VACIO:
                    tablero = result(tablero, (clicked_row, clicked_col), jugador)
                    sonido_clic.play()  # Reproducir sonido de clic

                    if terminal(tablero):
                        juego_terminado = True
                        mostrar_resultado(f"{jugador} ha ganado!")
                        sonido_ganar.play()  # Reproducir sonido de ganar
                        mostrar_boton_menu()
                    else:
                        jugador = O if jugador == X else X

            if modo_juego == "IA" and jugador == O and not juego_terminado:
                movimiento = mejor_movimiento_IA(tablero)
                tablero = result(tablero, movimiento, O)

                if terminal(tablero):
                    juego_terminado = True
                    mostrar_resultado(f"{O} ha ganado!")
                    sonido_ganar.play()  # Reproducir sonido de ganar
                    mostrar_boton_menu()
                else:
                    jugador = X

        draw_figures(tablero)
        pygame.display.update()


main()
