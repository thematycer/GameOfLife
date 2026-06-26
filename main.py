import pygame
import sys
from game import Game, Phase
from config import *
from grid import Grid
from special import SpecialType
from ui import draw_action_panel, draw_grid, draw_simulation_panel



def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game of Life")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    game = Game(num_players=2, action_interval=20)
    
    fonts = {
    "large":  pygame.font.SysFont(None, 22),
    "medium": pygame.font.SysFont(None, 18),
    "small":  pygame.font.SysFont(None, 15),
    }
    
    running = True
    selected_special_cell = None  # vybraná speciální buňka, například sýpka, pro umístění
    removing = False

    while running:
        # 1. vstup
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.grid.randomize(num_players=game.num_players)
                if event.key == pygame.K_RETURN:
                    selected_special_cell = None
                    removing = False
                    game.confirm_action()
                if game.phase == Phase.ACTION_PHASE:
                    if event.key == pygame.K_BACKSPACE:
                        removing = not removing  # přepni režim odstraňování
                    if event.key == pygame.K_a:
                        game.current_player_obj().buy_upgrade("aggression")
                    if event.key == pygame.K_s:
                        game.current_player_obj().buy_upgrade("resilience")
                    if event.key == pygame.K_g:
                        selected_special_cell = SpecialType.GRANARY
                    if event.key == pygame.K_m:
                        selected_special_cell = SpecialType.MINE_INACTIVE
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if removing:
                    game.remove_cell(row, col)
                elif selected_special_cell:
                    game.place_special(row, col, selected_special_cell)
                    selected_special_cell = None
                else:
                    game.place_cell(row, col)

        # 2. aktualizace
        game.tick()

        # 3. vykreslení
        screen.fill(COLOR_BACKGROUND)
        draw_grid(screen, game.grid)
        if game.phase == Phase.ACTION_PHASE:
            draw_action_panel(screen, game, fonts, removing, selected_special_cell)
        elif game.phase == Phase.SIMULATING:
            draw_simulation_panel(screen, game, fonts)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()