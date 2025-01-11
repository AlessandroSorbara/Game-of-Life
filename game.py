import pygame
import numpy as np
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_COLOR = (150, 150, 150)
ROWS = COLS = 80
BLOCK_SIZE = 10
BAR_SIZE = 50
WINDOW_WIDTH = ROWS * BLOCK_SIZE
WINDOW_HEIGHT = ROWS * BLOCK_SIZE + BAR_SIZE

def main():
    global SCREEN, CLOCK, running
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    CLOCK = pygame.time.Clock()
    
    matrix = np.zeros((ROWS, COLS), dtype=int)

    running = False
    while True:
        CLOCK.tick(60)

        SCREEN.fill(BLACK)
        draw_grid()

        if not running:
            draw_start(WHITE)
        else:
            draw_pause(WHITE)

        draw_matrix(matrix)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = pygame.mouse.get_pos()
                x_m = x // BLOCK_SIZE
                y_m = y // BLOCK_SIZE
                try:
                    if not running:
                        matrix[x_m][y_m] = 1 - matrix[x_m][y_m]
                except IndexError:
                    pass
                draw_matrix(matrix)

                if not running:
                    if pygame.Rect(WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT - BAR_SIZE + 10, 40, 30).collidepoint(x, y):
                        running = True
                        draw_start(BLACK)
                        draw_pause(WHITE)
                else:
                    if pygame.Rect(WINDOW_WIDTH // 2 - 20, WINDOW_HEIGHT - BAR_SIZE + 10, 40, 30).collidepoint(x, y):
                        running = False
                        draw_pause(BLACK)
                        draw_start(WHITE)

        if running:
            new_matrix = matrix.copy()
            for x in range(len(matrix)):
                for y in range(len(matrix[0])):
                    cell_state = matrix[x][y]
                    neighbours_count = 0
                    for i in [-1, 0, 1]:
                        for j in [-1, 0, 1]:
                            if i == 0 and j == 0:
                                continue
                            nx, ny = x + i, y + j
                            if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]):
                                neighbours_count += matrix[nx][ny]

                    if cell_state == 1:
                        if neighbours_count < 2 or neighbours_count > 3:
                            new_matrix[x][y] = 0     
                    else:
                        if neighbours_count == 3:
                            new_matrix[x][y] = 1
            matrix = new_matrix     

        pygame.display.update()


def draw_grid():
    for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
        for y in range(0, WINDOW_HEIGHT - BAR_SIZE, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, GRID_COLOR, rect, 1)


def draw_matrix(matrix):
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            if matrix[x][y] == 1:
                pygame.draw.rect(SCREEN, WHITE, rect)


def draw_start(color):
    points = [(WINDOW_WIDTH // 2 - 15, WINDOW_HEIGHT - BAR_SIZE + 10), (WINDOW_WIDTH // 2 + 15, WINDOW_HEIGHT - BAR_SIZE + 25), (WINDOW_WIDTH // 2 - 15, WINDOW_HEIGHT - BAR_SIZE + 40)]
    pygame.draw.polygon(SCREEN, color, points)
   

def draw_pause(color):
    pygame.draw.rect(SCREEN, color, (WINDOW_WIDTH // 2 - 15, WINDOW_HEIGHT - BAR_SIZE + 15, 10, 20))
    pygame.draw.rect(SCREEN, color, (WINDOW_WIDTH // 2 + 5, WINDOW_HEIGHT - BAR_SIZE + 15, 10, 20))

if __name__ == '__main__':
    main()