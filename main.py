import pygame
import sys
from game import Game, Phase
from config import *
from setup import SetupScreen
from special import SpecialType
from ui import draw_action_panel, draw_game_over_panel, draw_grid, draw_simulation_panel, draw_setup
from modes import DominanceMode



def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game of Life")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    game = None
    
    fonts = {
    "large":  pygame.font.SysFont(None, 22),
    "medium": pygame.font.SysFont(None, 18),
    "small":  pygame.font.SysFont(None, 15),
    }
    
    running = True
    selected_special_cell = None  # vybraná speciální buňka, například sýpka, pro umístění
    removing = False
    setup = SetupScreen()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif game is None:
                # --- SETUP ---
                if event.type == pygame.KEYDOWN:
                    done = setup.handle_key(event.key)
                    if done:
                        game = setup.build_game()
                        screen = pygame.display.set_mode((game.window_width, game.window_height))
                if event.type == pygame.TEXTINPUT:
                    setup.handle_text(event.text)

            elif game.phase == Phase.GAME_OVER:
                # --- KONEC HRY ---
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game = None
                        setup = SetupScreen()

            elif game.phase == Phase.SIMULATING:
                # --- SIMULACE ---
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game.grid.randomize(num_players=game.num_players)

            elif game.phase == Phase.ACTION_PHASE:
                # --- FÁZE AKCE ---
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        selected_special_cell = None
                        removing = False
                        game.confirm_action()
                    elif event.key == pygame.K_BACKSPACE:
                        removing = not removing
                    elif event.key == pygame.K_a:
                        game.current_player_obj().buy_upgrade("aggression")
                    elif event.key == pygame.K_s:
                        game.current_player_obj().buy_upgrade("resilience")
                    elif event.key == pygame.K_g:
                        selected_special_cell = SpecialType.GRANARY
                    elif event.key == pygame.K_m:
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
        
        screen.fill(COLOR_BACKGROUND)
        
        
        # 2. aktualizace
        if game is not None:
            game.tick()

            # 3. vykreslení
            draw_grid(screen, game.grid)
            if game.phase == Phase.ACTION_PHASE:
                draw_action_panel(screen, game, fonts, removing, selected_special_cell)
            elif game.phase == Phase.SIMULATING:
                draw_simulation_panel(screen, game, fonts)
            elif game.phase == Phase.GAME_OVER:
                draw_game_over_panel(screen, game, fonts)
        else:
            draw_setup(screen, setup, fonts)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()