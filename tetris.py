import pygame, sys, random

# Pygame und Fenster einrichten
pygame.init()
CELL_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20  # Die Höhe des Spielfelds (20 Zeilen)
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
pygame.display.set_caption("Tetris")

# Farben definieren
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Die verschiedenen Tetromino-Formen (I, O, L, J, S, Z, T)
tetrominos = [
    [(1, 5), (0, 4), (0, 5), (0, 6)],
    [(1, 5), (0, 5), (0, 6), (1, 6)],
    [(1, 4), (0, 4), (0, 5), (0, 6)],
    [(1, 6), (0, 4), (0, 5), (0, 6)],
    [(1, 5), (0, 4), (0, 5), (1, 6)],
    [(1, 5), (0, 5), (0, 6), (1, 4)],
    [(0, 4), (0, 5), (1, 5), (1, 6)],
]

# Spielfeld ist ein leeres Grid
grid = [[0] * GRID_HEIGHT for _ in range(GRID_WIDTH)]


# Funktion, um das Spiel zu beenden, wenn das Spielfeld voll ist
def game_over():
    print("Game Over")
    pygame.quit()
    sys.exit()


# Prüfen, ob sich ein Tetromino bewegen kann
def is_valid_move(position, offset):
    for i in range(4):
        x = position[i][0] + offset[0]
        y = position[i][1] + offset[1]
        if y < 0:
            continue  # Wenn oberhalb des Spielfelds, überspringen
        if x < 0 or x >= GRID_WIDTH or y >= GRID_HEIGHT:
            return False  # Geht über den Rand hinaus
        if grid[x][y]:  # Kollidiert mit einem feststehenden Block
            return False
    return True


# Drehen des Tetrominos (falls Platz dafür)
def rotate(tetromino):
    cx, cy = tetromino[0]  # Mittelpunkt zum Drehen
    new_position = [(cx + cy - y, cy - cx + x) for x, y in tetromino]
    if is_valid_move(new_position, [0, 0]):
        return new_position
    return tetromino  # Bleibt wie es ist, wenn ungültig


# Zufälliges Tetromino auswählen
def get_random_tetromino():
    return tetrominos[random.randint(0, len(tetrominos) - 1)]


# Funktion, um das aktuelle Tetromino zu fixieren
def fix_tetromino(tetromino):
    for x, y in tetromino:
        if y >= 0:  # Nur Zellen innerhalb des sichtbaren Spielfelds festsetzen
            grid[x][y] = 1
    clear_full_rows()  # Reihen löschen, nachdem ein Tetromino fixiert wurde


# Funktion, um vollständige Reihen zu löschen
def clear_full_rows():
    global grid
    new_grid = [[0] * GRID_HEIGHT for _ in range(GRID_WIDTH)]
    new_row_index = GRID_HEIGHT - 1

    # Überprüfe jede Zeile von unten nach oben
    for y in range(GRID_HEIGHT - 1, -1, -1):
        row_filled = all(grid[x][y] for x in range(GRID_WIDTH))
        if not row_filled:
            # Kopiere die Zeile in das neue Grid
            for x in range(GRID_WIDTH):
                new_grid[x][new_row_index] = grid[x][y]
            new_row_index -= 1

    grid = new_grid  # Ersetze das alte Grid durch das neue


# Funktion, um Game Over zu überprüfen, wenn ein neues Tetromino erzeugt wird
def check_game_over(tetromino):
    for x, y in tetromino:
        if y >= 0 and grid[x][y]:  # Kollision in der obersten Zeile
            game_over()


# Aktuelles Tetromino und Bewegungsrichtung
current_tetromino = get_random_tetromino()
movement_vector = [0, 0]  # Seitliche Bewegung
drop_vector = [0, 1]  # Automatisch nach unten
fast_drop = False  # Schneller Fall, wenn True

# Hauptspiel-Schleife
while True:
    # Tastendrücke abfragen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and is_valid_move(current_tetromino, [-1, 0]):
                movement_vector = [-1, 0]  # Nach links
            elif event.key == pygame.K_RIGHT and is_valid_move(current_tetromino, [1, 0]):
                movement_vector = [1, 0]  # Nach rechts
            elif event.key == pygame.K_UP:
                current_tetromino = rotate(current_tetromino)  # Rotation
            elif event.key == pygame.K_DOWN:
                fast_drop = True  # Aktiviert den schnellen Fall

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                fast_drop = False  # Deaktiviert den schnellen Fall

    # Automatische Abwärtsbewegung
    fall_speed = [0, 2] if fast_drop else drop_vector  # Schneller Fall, wenn `fast_drop` aktiviert ist

    # Wenn gültig, wende das `fall_speed` an
    if is_valid_move(current_tetromino, fall_speed):
        current_tetromino = [(x + fall_speed[0], y + fall_speed[1]) for x, y in current_tetromino]
    else:
        # Wenn das Tetromino nicht mehr fallen kann, im Grid fixieren und Game Over prüfen
        fix_tetromino(current_tetromino)
        current_tetromino = get_random_tetromino()  # Neues Tetromino
        check_game_over(current_tetromino)  # Überprüft Game Over beim Erstellen des neuen Tetrominos

    # Seitliche Bewegung anwenden, falls gültig
    if is_valid_move(current_tetromino, movement_vector):
        current_tetromino = [(x + movement_vector[0], y) for x, y in current_tetromino]

    # Bildschirm leeren und Tetrominos zeichnen
    screen.fill(BLACK)
    for x, y in current_tetromino:
        pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Feststehende Blöcke aus dem Grid zeichnen
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            if grid[x][y]:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()  # Zeigt das neu gezeichnete Bild
    pygame.time.delay(300)  # Tempo des Spiels

    # Bewegung zurücksetzen, damit es nicht dauerhaft in eine Richtung geht
    movement_vector = [0, 0]
