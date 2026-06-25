import pygame
import sys
from game import Game, Phase
from config import *
from grid import Grid


def draw_grid(screen: pygame.Surface, grid: Grid):
    for row in range(grid.height):
        for col in range(grid.width):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            owner = grid.cells[row, col]
            color = PLAYER_COLORS[owner]  # 0 = pozadí, 1+ = hráči
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

def show_ui(screen: pygame.Surface, game: Game, font: pygame.font.Font):
    if game.phase == Phase.SIMULATING:
        return
    if game.phase == Phase.ACTION_PHASE:
        player = game.current_player_obj()

        # pozadí pro text
        pygame.draw.rect(screen, (30, 30, 30), (0, 0, WINDOW_WIDTH, 60))

        # vykresli informace o hráči
        color = PLAYER_COLORS[player.id]
        name_text = f"{player.name} | Skóre: {player.score}"
        screen.blit(font.render(name_text, True, color), (10, 10))

        # dostupné upgrady
        # dostupné upgrady
        agg_cost = player.upgrade_cost("aggression")
        res_cost = player.upgrade_cost("resilience")
        upgrades_text = f"[A] Agresivita {player.aggression} -> cena za vylepšení {player.aggression + 1} ({agg_cost} bodů)   [S] Odolnost {player.resilience} -> cena za vylepšení {player.resilience + 1} ({res_cost} bodů)   [Enter] Potvrdit"
        screen.blit(font.render(upgrades_text, True, (200, 200, 200)), (10, 35))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Game of Life")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)

    game = Game(num_players=2, action_interval=20)

    running = True

    while running:
        # 1. vstup
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.grid.randomize(num_players=game.num_players)
                if event.key == pygame.K_RETURN:
                    game.confirm_action()
                if game.phase == Phase.ACTION_PHASE:
                    if event.key == pygame.K_a:
                        game.current_player_obj().buy_upgrade("aggression")
                    if event.key == pygame.K_s:
                        game.current_player_obj().buy_upgrade("resilience")
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                game.place_cell(row, col)

        # 2. aktualizace
        game.tick()

        # 3. vykreslení
        screen.fill(COLOR_BACKGROUND)
        draw_grid(screen, game.grid)
        if game.phase == Phase.ACTION_PHASE:
            show_ui(screen, game, font)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()