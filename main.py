import pygame
import sys
from grid import Grid
from config import *

def draw_grid(screen: pygame.Surface, grid: Grid):
    for row in range(grid.height):
        for col in range(grid.width):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            owner = grid.cells[row, col]
            if owner > 0:
                color = PLAYER_COLORS[owner - 1]  # index hráče je o 1 menší než ID hráče
            else:
                color = COLOR_BACKGROUND
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
def main():
    pygame.init() # inicializace Pygame
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # nastavení velikosti okna
    pygame.display.set_caption("Game of Life") # nastavení názvu okna
    clock = pygame.time.Clock() # nastavení FPS

    grid = Grid(GRID_WIDTH, GRID_HEIGHT) 
    grid.randomize(num_players=3) # zatím náhodně naplníme mřížku živými buňkami

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
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                # přepni buňku: živá → mrtvá, mrtvá → živá
                grid.cells[row, col] = 1 - grid.cells[row, col]

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