import pygame
from config import *
from grid import Grid
from special import SpecialType
import numpy as np

def draw_action_panel(screen, game, fonts, removing, selected_special):
    player = game.current_player_obj()
    color = PLAYER_COLORS[player.id]
    x = WINDOW_WIDTH - PANEL_WIDTH  # začátek panelu

    # pozadí panelu
    pygame.draw.rect(screen, (25, 25, 25), (x, 0, PANEL_WIDTH, WINDOW_HEIGHT))
    pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, WINDOW_HEIGHT))

    y = 16

    # --- hráč a skóre ---
    pygame.draw.circle(screen, color, (x + 18, y + 8), 6)
    screen.blit(fonts["large"].render(player.name, True, color), (x + 30, y))
    y += 24
    screen.blit(fonts["small"].render(f"Skóre: {player.score} bodů", True, (150, 150, 150)), (x + 10, y))
    y += 28

    # --- oddělovač ---
    pygame.draw.line(screen, (50, 50, 50), (x + 10, y), (WINDOW_WIDTH - 10, y))
    y += 12

    # --- upgrady ---
    screen.blit(fonts["small"].render("UPGRADY", True, (80, 80, 80)), (x + 10, y))
    y += 18

    for key, label, attr in [("A", "Agresivita", "aggression"), ("S", "Odolnost", "resilience")]:
        level = getattr(player, attr)
        cost = player.upgrade_cost(attr)
        affordable = player.score >= cost

        name_color = (200, 200, 200) if affordable else (80, 80, 80)
        screen.blit(fonts["medium"].render(f"[{key}] {label}  lv.{level}", True, name_color), (x + 10, y))
        y += 18
        cost_color = color if affordable else (60, 60, 60)
        screen.blit(fonts["small"].render(f"     → {cost} bodů", True, cost_color), (x + 10, y))
        y += 22

    y += 4
    pygame.draw.line(screen, (50, 50, 50), (x + 10, y), (WINDOW_WIDTH - 10, y))
    y += 12

    # --- akce ---
    screen.blit(fonts["small"].render("AKCE", True, (80, 80, 80)), (x + 10, y))
    y += 18

    granary_color = color if player.score >= GRANARY_COST else (60, 60, 60)
    screen.blit(fonts["medium"].render("[G] Sýpka", True, granary_color), (x + 10, y))
    y += 18
    screen.blit(fonts["small"].render(f"     → {GRANARY_COST} bodů", True, granary_color), (x + 10, y))
    y += 22

    screen.blit(fonts["medium"].render("[X] Smazat buňku", True, (200, 200, 200)), (x + 10, y))
    y += 18
    screen.blit(fonts["small"].render("     → +10 bodů", True, (100, 150, 100)), (x + 10, y))
    y += 28

    pygame.draw.line(screen, (50, 50, 50), (x + 10, y), (WINDOW_WIDTH - 10, y))
    y += 12

    # --- aktuální mód ---
    screen.blit(fonts["small"].render("AKTUÁLNÍ MÓD", True, (80, 80, 80)), (x + 10, y))
    y += 18
    if removing:
        mode_text = "Mazání buněk"
    elif selected_special == SpecialType.GRANARY:
        mode_text = "Umístit sýpku"
    else:
        mode_text = "Umístit buňku"
    screen.blit(fonts["medium"].render(mode_text, True, color), (x + 10, y))

    # --- enter dole ---
    enter_y = WINDOW_HEIGHT - 36
    pygame.draw.line(screen, (50, 50, 50), (x + 10, enter_y - 8), (WINDOW_WIDTH - 10, enter_y - 8))
    screen.blit(fonts["medium"].render("[Enter] Potvrdit tah", True, (120, 120, 120)), (x + 10, enter_y))

def draw_simulation_panel(screen, game, fonts):
    x = WINDOW_WIDTH - PANEL_WIDTH

    # pozadí panelu
    pygame.draw.rect(screen, (25, 25, 25), (x, 0, PANEL_WIDTH, WINDOW_HEIGHT))
    pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, WINDOW_HEIGHT))

    y = 16
    screen.blit(fonts["small"].render("PŘEHLED", True, (80, 80, 80)), (x + 10, y))
    y += 18

    for player in game.players:
        color = PLAYER_COLORS[player.id]
        cell_count = int(np.sum(game.grid.cells == player.id))
        granary_count = int(np.sum(
            (game.grid.special == SpecialType.GRANARY.value) &
            (game.grid.cells == player.id)
        ))

        # jméno hráče
        pygame.draw.circle(screen, color, (x + 18, y + 7), 5)
        screen.blit(fonts["medium"].render(player.name, True, color), (x + 30, y))
        y += 18
        screen.blit(fonts["small"].render(f"  Buňky: {cell_count}", True, (150, 150, 150)), (x + 10, y))
        y += 16
        screen.blit(fonts["small"].render(f"  Sýpky: {granary_count}", True, (150, 150, 150)), (x + 10, y))
        y += 20

        pygame.draw.line(screen, (50, 50, 50), (x + 10, y), (WINDOW_WIDTH - 10, y))
        y += 12

def draw_grid(screen: pygame.Surface, grid: Grid):
    for row in range(grid.height):
        for col in range(grid.width):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            owner = grid.cells[row, col]
            color = PLAYER_COLORS[owner]  # 0 = pozadí, 1+ = hráči
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
            if grid.special[row, col] == SpecialType.GRANARY.value:
                # vykresli sýpku jako bílý čtverec uprostřed buňky
                center_x = x + CELL_SIZE // 2
                center_y = y + CELL_SIZE // 2
                pygame.draw.rect(screen, (255, 255, 255), (center_x - 2, center_y - 2, 4, 4))