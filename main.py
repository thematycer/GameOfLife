import pygame
import sys
from grid import Grid
from config import *

def draw_grid(screen: pygame.Surface, grid: Grid):
    for row in range(grid.height):
        for col in range(grid.width):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            if grid.cells[row, col] == 1:
                pygame.draw.rect(screen, COLOR_ALIVE, (x, y, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, COLOR_BACKGROUND, (x, y, CELL_SIZE, CELL_SIZE))
def main():
    pygame.init() # inicializace Pygame
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # nastavení velikosti okna
    pygame.display.set_caption("Game of Life") # nastavení názvu okna
    clock = pygame.time.Clock() # nastavení FPS

    grid = Grid(GRID_WIDTH, GRID_HEIGHT) 
    grid.randomize() # zatím náhodně naplníme mřížku živými buňkami

    running = True
    paused = False

    while running:
        # 1. vstup
        for event in pygame.event.get():# vrací seznam všech událostí, které se staly od posledního volání
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_r:
                    grid.randomize()

        # 2. aktualizace
        if not paused:
            grid.next_generation()

        # 3. vykreslení
        screen.fill(COLOR_BACKGROUND)# smaže obsah obrazovky
        draw_grid(screen, grid) # vykreslí mřížku na obrazovku
        pygame.display.flip()# aktualizuje obsah obrazovky

        clock.tick(FPS) # nastaví rychlost hry na FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()