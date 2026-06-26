import pygame
from config import *
from grid import Grid
from special import SpecialType
import numpy as np

def draw_action_panel(screen, game, fonts, removing, selected_special):
    player = game.current_player_obj()
    color = PLAYER_COLORS[player.id]
    x = game.window_width - PANEL_WIDTH  # začátek panelu

    # pozadí panelu
    pygame.draw.rect(screen, (25, 25, 25), (x, 0, PANEL_WIDTH, game.window_height))
    pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, game.window_height))

    y = 16

    # --- hráč a skóre ---
    pygame.draw.circle(screen, color, (x + 18, y + 8), 6)
    screen.blit(fonts["large"].render(player.name, True, color), (x + 30, y))
    y += 24
    screen.blit(fonts["small"].render(f"Skóre: {player.score} bodů", True, (150, 150, 150)), (x + 10, y))
    y += 28

    # --- oddělovač ---
    pygame.draw.line(screen, (50, 50, 50), (x + 10, y), (game.window_width - 10, y))
    y += 12

    # --- upgrady ---
    screen.blit(fonts["small"].render("UPGRADY", True, (80, 80, 80)), (x + 10, y))
    y += 18

    for key, label, attr in [("A", "Agresivita", "aggression"), ("S", "Odolnost", "resilience")]:
        level = getattr(player, attr)
        cost = player.upgrade_cost(attr)
        affordable = player.score >= cost and level <= MAX_UPGRADE_LEVEL

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

    mine_color = color if player.score >= MINE_COST else (60, 60, 60)
    screen.blit(fonts["medium"].render("[M] Mina", True, mine_color), (x + 10, y))
    y += 18
    screen.blit(fonts["small"].render(f"     → {MINE_COST} bodů", True, mine_color), (x + 10, y))
    y += 22

    factory_color = color if player.score >= FACTORY_COST else (60, 60, 60)
    screen.blit(fonts["medium"].render("[F] Továrna", True, factory_color), (x + 10, y))
    y += 18
    screen.blit(fonts["small"].render(f"     → {FACTORY_COST} bodů", True, factory_color), (x + 10, y))
    y += 22

    screen.blit(fonts["medium"].render("[X] Smazat buňku", True, (200, 200, 200)), (x + 10, y))
    y += 18
    screen.blit(fonts["small"].render("     → +10 bodů", True, (100, 150, 100)), (x + 10, y))
    y += 28

    pygame.draw.line(screen, (50, 50, 50), (x + 10, y), (game.window_width - 10, y))
    y += 12

    # --- aktuální mód ---
    screen.blit(fonts["small"].render("AKTUÁLNÍ MÓD", True, (80, 80, 80)), (x + 10, y))
    y += 18
    if removing:
        mode_text = "Mazání buněk"
    elif selected_special == SpecialType.GRANARY:
        mode_text = "Umístit sýpku"
    elif selected_special == SpecialType.MINE_INACTIVE:
        mode_text = "Umístit minu"
    else:
        mode_text = "Umístit buňku"
    screen.blit(fonts["medium"].render(mode_text, True, color), (x + 10, y))

    # --- enter dole ---
    enter_y = game.window_height - 36
    pygame.draw.line(screen, (50, 50, 50), (x + 10, enter_y - 8), (game.window_width - 10, enter_y - 8))
    screen.blit(fonts["medium"].render("[Enter] Potvrdit tah", True, (120, 120, 120)), (x + 10, enter_y))

def draw_simulation_panel(screen, game, fonts):
    x = game.window_width - PANEL_WIDTH

    # pozadí panelu
    pygame.draw.rect(screen, (25, 25, 25), (x, 0, PANEL_WIDTH, game.window_height))
    pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, game.window_height))

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

        pygame.draw.line(screen, (50, 50, 50), (x + 10, y), (game.window_width - 10, y))
        y += 12

def draw_grid(screen: pygame.Surface, grid: Grid):
    for row in range(grid.height):
        for col in range(grid.width):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            owner = grid.cells[row, col]
            color = PLAYER_COLORS[owner]
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

            s = grid.special[row, col]
            if s == SpecialType.GRANARY.value:
                cx, cy = x + CELL_SIZE // 2, y + CELL_SIZE // 2
                pygame.draw.rect(screen, (255, 255, 255), (cx - 2, cy - 2, 4, 4))
            elif s == SpecialType.FLAG.value:
                pygame.draw.rect(screen, (255, 215, 0), 
                    (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4), 2)
            elif s == SpecialType.MINE_INACTIVE.value:
                pygame.draw.line(screen, (150, 150, 150), (x + 2, y + 2), (x + CELL_SIZE - 2, y + CELL_SIZE - 2), 2)
                pygame.draw.line(screen, (150, 150, 150), (x + CELL_SIZE - 2, y + 2), (x + 2, y + CELL_SIZE - 2), 2)
            elif s == SpecialType.MINE_ACTIVE.value:
                pygame.draw.line(screen, (255, 80, 80), (x + 2, y + 2), (x + CELL_SIZE - 2, y + CELL_SIZE - 2), 2)
                pygame.draw.line(screen, (255, 80, 80), (x + CELL_SIZE - 2, y + 2), (x + 2, y + CELL_SIZE - 2), 2)
            elif s == SpecialType.FACTORY.value:
                cx, cy = x + CELL_SIZE // 2, y + CELL_SIZE // 2
                pygame.draw.rect(screen, (255, 165, 0), (cx - 3, cy - 3, 6, 6))
    
def draw_game_over_panel(screen, game, fonts):
    x = game.window_width - PANEL_WIDTH

    # pozadí panelu
    pygame.draw.rect(screen, (25, 25, 25), (x, 0, PANEL_WIDTH, game.window_height))
    pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, game.window_height))

    y = 16

    # --- nadpis ---
    screen.blit(fonts["large"].render("KONEC HRY", True, (200, 200, 200)), (x + 10, y))
    y += 20
    screen.blit(fonts["small"].render(game.mode.description(), True, (80, 80, 80)), (x + 10, y))
    y += 24

    pygame.draw.line(screen, (50, 50, 50), (x + 10, y), (game.window_width - 10, y))
    y += 12

    # --- pořadí ---
    screen.blit(fonts["small"].render("POŘADÍ", True, (80, 80, 80)), (x + 10, y))
    y += 18

    for i, entry in enumerate(game.standings):
        player = entry["player"]
        color = PLAYER_COLORS[player.id]

        # číslo místa
        place_color = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]  # zlato, stříbro, bronz
        rank_color = place_color[i] if i < 3 else (120, 120, 120)
        screen.blit(fonts["medium"].render(f"#{i + 1}", True, rank_color), (x + 10, y))

        # jméno hráče
        pygame.draw.circle(screen, color, (x + 36, y + 7), 5)
        screen.blit(fonts["medium"].render(player.name, True, color), (x + 48, y))
        y += 20

        # buňky a skóre
        if "flag_score" in entry:
            screen.blit(fonts["small"].render(
                f"  Body za vlajky: {entry['flag_score']}", True, (150, 150, 150)), (x + 10, y))
        else:
            y += 16
            screen.blit(fonts["small"].render(
                f"  Buňky: {entry['cells']}", True, (150, 150, 150)), (x + 10, y))
            y += 16
            screen.blit(fonts["small"].render(
                f"  Skóre: {entry['score']}", True, (150, 150, 150)), (x + 10, y))
        y += 20
        

        pygame.draw.line(screen, (50, 50, 50), (x + 10, y), (game.window_width - 10, y))
        y += 12

    # --- restart dole ---
    restart_y = game.window_height - 36
    pygame.draw.line(screen, (50, 50, 50), (x + 10, restart_y - 8), (game.window_width - 10, restart_y - 8))
    screen.blit(fonts["medium"].render("[R] Nová hra", True, (120, 120, 120)), (x + 10, restart_y))

def draw_setup(screen, setup, fonts):
    cx = WINDOW_WIDTH // 2  # střed obrazovky

    # --- nadpis ---
    y = 60
    title = fonts["large"].render("GAME OF LIFE", True, (200, 200, 200))
    screen.blit(title, (cx - title.get_width() // 2, y))
    y += 40

    if not setup.naming:
        # --- výběr nastavení ---
        subtitle = fonts["small"].render("Nastav hru a stiskni Enter", True, (80, 80, 80))
        screen.blit(subtitle, (cx - subtitle.get_width() // 2, y))
        y += 40

        for i, option in enumerate(setup.options):
            is_selected = i == setup.selected
            label_color = (200, 200, 200) if is_selected else (100, 100, 100)
            value_color = (255, 255, 255) if is_selected else (150, 150, 150)

            # zvýraznění vybrané položky
            if is_selected:
                pygame.draw.rect(screen, (40, 40, 40),
                    (cx - 180, y - 4, 360, 26), border_radius=4)

            label = fonts["medium"].render(option.label, True, label_color)
            screen.blit(label, (cx - 170, y))

            # šipky + hodnota
            arrow_left  = fonts["medium"].render("<", True, value_color)
            arrow_right = fonts["medium"].render(">", True, value_color)
            value_text  = fonts["medium"].render(str(option.value), True, value_color)

            screen.blit(arrow_left,  (cx + 60, y))
            screen.blit(value_text,  (cx + 85, y))
            screen.blit(arrow_right, (cx + 85 + value_text.get_width() + 4, y))

            y += 36

    else:
        # --- zadávání jmen ---
        subtitle = fonts["small"].render("Zadej jména hráčů, Enter = další", True, (80, 80, 80))
        screen.blit(subtitle, (cx - subtitle.get_width() // 2, y))
        y += 40

        for i, name in enumerate(setup.player_names):
            is_current = i == setup.naming_index
            color = PLAYER_COLORS[i + 1]

            pygame.draw.circle(screen, color, (cx - 140, y + 8), 5)

            if is_current:
                # aktivní pole – s kurzorem
                pygame.draw.rect(screen, (40, 40, 40),
                    (cx - 120, y - 4, 260, 26), border_radius=4)
                display_name = name + "|"  # kurzor
                name_color = (255, 255, 255)
            else:
                display_name = name if name else f"Hráč {i+1}"
                name_color = (150, 150, 150)

            screen.blit(fonts["medium"].render(display_name, True, name_color), (cx - 110, y))
            y += 36