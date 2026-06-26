''' 
soubor pro testování hry Game of Life
'''
import numpy as np
import pytest
from config import CELL_COST, FACTORY_INCOME, GRANARY_COST, REFUND_MULTIPLIER, UPGRADE_COST_BASE
from grid import Grid
from game import Game, Phase
from player import Player
from special import SpecialType, mine_explosion
from modes import DominanceMode, EliminationMode, FlagsMode

# pomocné funkce
def make_game(num_players=2, ticks=100, random_start=False):
    return Game(
        num_players=num_players,
        action_interval=20,
        mode=DominanceMode(max_ticks=ticks),
        start_score=200,
        random_start=random_start,
    )

def set_blinker(grid, row, col):
    """Vodorovný blinker osciluje každý tick."""
    grid.cells[row, col - 1] = 1
    grid.cells[row, col]     = 1
    grid.cells[row, col + 1] = 1


#Základní pravidla hry života
class TestGridBasics:
    def test_blinker_oscillates(self):
        """Blinker se po jednom ticku otočí na svislý a pak vodorovný."""
        g = Grid(10, 10)
        set_blinker(g, 5, 5)
        g.next_generation(lambda r, c: 1, lambda *a: None)
        #svislý
        assert g.cells[4, 5] == 1
        assert g.cells[5, 5] == 1
        assert g.cells[6, 5] == 1
        assert g.cells[5, 4] == 0
        assert g.cells[5, 6] == 0
        # vorodorvný
        g.next_generation(lambda r, c: 1, lambda *a: None)
        assert g.cells[5, 4] == 1
        assert g.cells[5, 5] == 1
        assert g.cells[5, 6] == 1
        assert g.cells[4, 5] == 0
        assert g.cells[6, 5] == 0

    def test_lonely_cell_dies(self):
        """Osamělá buňka zemře."""
        g = Grid(10, 10)
        g.cells[5, 5] = 1
        g.cells[8, 8] = 1
        g.next_generation(lambda r, c: 1, lambda *a: None)
        assert g.cells[5, 5] == 0
        assert g.cells[8, 8] == 0
        
    def test_stable_block(self):
        """2x2 blok zůstane stabilní."""
        g = Grid(10, 10)
        g.cells[4, 4] = 1
        g.cells[4, 5] = 1
        g.cells[5, 4] = 1
        g.cells[5, 5] = 1
        g.next_generation(lambda r, c: 1, lambda *a: None)
        g.next_generation(lambda r, c: 1, lambda *a: None)
        g.next_generation(lambda r, c: 1, lambda *a: None)
        g.next_generation(lambda r, c: 1, lambda *a: None)
        g.next_generation(lambda r, c: 1, lambda *a: None)
        assert g.cells[4, 4] == 1
        assert g.cells[4, 5] == 1
        assert g.cells[5, 4] == 1
        assert g.cells[5, 5] == 1

    def test_dead_cell_with_3_neighbors_revives(self):
        """Mrtvá buňka se 3 sousedy oživí."""
        g = Grid(10, 10)
        g.cells[5, 4] = 1
        g.cells[5, 5] = 1
        g.cells[5, 6] = 1
        g.next_generation(lambda r, c: 1, lambda *a: None)
        assert g.cells[4, 5] == 1
        assert g.cells[6, 5] == 1

    def test_overpopulation_kills(self):
        """Buňka s více než 3 sousedy zemře."""
        g = Grid(10, 10)
        # střed má 4 sousedy
        g.cells[5, 5] = 1
        g.cells[4, 5] = 1
        g.cells[6, 5] = 1
        g.cells[5, 4] = 1
        g.cells[5, 6] = 1
        g.next_generation(lambda r, c: 1, lambda *a: None)
        assert g.cells[5, 5] == 0


# test dominantní váhy
class TestDominantNeighbor:
    def test_majority_wins(self):
        """Hráč s více sousedy dostane buňku."""
        game = make_game(num_players=3)
        game.grid.cells[4, 4] = 1
        game.grid.cells[4, 5] = 1
        game.grid.cells[4, 6] = 2
        game.grid.cells[5, 6] = 3
        result = game.dominant_neighbor(5, 5)
        assert result == 1

    def test_aggression_bonus(self):
        """Agresivita zvýší váhu sousedů."""
        game = make_game()
        game.players[1].aggression = 4  # hráč 2: bonus 1 + 4*0.5 = 3 na souseda
        game.grid.cells[4, 4] = 1  # hráč 1
        game.grid.cells[4, 5] = 1  # hráč 1
        game.grid.cells[4, 6] = 2  # hráč 2 – jen jeden, ale s bonusem co mu dává převahu
        # hráč 1: 2 * 1.0 = 2.0, hráč 2: 1 * 3.0 = 3.0 → hráč 2 vyhraje
        result = game.dominant_neighbor(5, 5)
        assert result == 2

    def test_empty_neighbors_returns_zero(self):
        """Bez živých sousedů vrátí 0."""
        game = make_game()
        result = game.dominant_neighbor(5, 5)
        assert result == 0

# test ekonomiky
class TestEconomy:
    def test_buy_upgrade_deducts_score(self):
        p = Player(id=1, name="Test", score=UPGRADE_COST_BASE*4)
        p.buy_upgrade("aggression")
        assert p.aggression == 1
        assert p.score == UPGRADE_COST_BASE*3  # 200 - 50
    
    def test_multiple_purchases(self):
        p = Player(id=1, name="Test", score=UPGRADE_COST_BASE*4)
        p.buy_upgrade("aggression")
        assert p.aggression == 1
        assert p.score == UPGRADE_COST_BASE*3  # UPGRADE_COST_BASE*4 - UPGRADE_COST_BASE
        p.buy_upgrade("aggression")
        assert p.aggression == 2
        assert p.score == UPGRADE_COST_BASE  # UPGRADE_COST_BASE*4-UPGRADE_COST_BASE*3

    def test_buy_upgrade_insufficient_score(self):
        p = Player(id=1, name="Test", score=10)
        result = p.buy_upgrade("aggression")
        assert result == False
        assert p.aggression == 0
    
    def test_max_upgrade_level(self):
        """Nelze koupit více než MAX_UPGRADE_LEVEL."""
        from config import MAX_UPGRADE_LEVEL
        p = Player(id=1, name="Test", score=999999)
        for _ in range(MAX_UPGRADE_LEVEL + 5):
            p.buy_upgrade("aggression")
        assert p.aggression == MAX_UPGRADE_LEVEL

    def test_upgrade_cost_scales(self):
        """Cena upgradu roste s levelem."""
        p = Player(id=1, name="Test", score=0)
        cost_0 = p.upgrade_cost("aggression")
        p.aggression = 1
        cost_1 = p.upgrade_cost("aggression")
        assert cost_1 > cost_0

    def test_buy_resilience(self):
        """Odolnost lze koupit stejně jako agresivitu."""
        p = Player(id=1, name="Test", score=UPGRADE_COST_BASE*4)
        p.buy_upgrade("resilience")
        assert p.resilience == 1
        assert p.score == UPGRADE_COST_BASE*3

# akční fáze
class TestGamePhases:
    def test_place_cell_costs_score(self):
        from config import CELL_COST
        game = make_game()
        game.grid.cells[5, 5] = 0
        game.players[0].score = CELL_COST
        score_before = game.players[0].score
        game.place_cell(5, 5)
        assert game.players[0].score == score_before - CELL_COST
        assert game.grid.cells[5, 5] == 1
        assert  game.players[0].score == 0

    def test_cannot_place_without_score(self):
        game = make_game()
        game.players[0].score = 0
        game.place_cell(5, 5)
        assert game.grid.cells[5, 5] == 0

    def test_confirm_action_cycles_players(self):
        game = make_game(num_players=3)
        assert game.current_player == 0
        game.confirm_action()
        assert game.current_player == 1
        game.confirm_action()
        assert game.current_player == 2
        game.confirm_action()
        assert game.current_player == 0
        assert game.phase == Phase.SIMULATING

    def test_remove_cell_refund(self):
        game = make_game()
        game.grid.cells[5, 5] = 1
        score_before = game.players[0].score
        game.remove_cell(5, 5)
        assert game.players[0].score == score_before + CELL_COST * REFUND_MULTIPLIER
        assert game.grid.cells[5, 5] == 0
    
    def test_remove_granary_refund(self):
        game = make_game()
        game.grid.cells[5, 5] = 1
        game.grid.special[5, 5] = SpecialType.GRANARY.value
        score_before = game.players[0].score
        game.remove_cell(5, 5)
        assert game.players[0].score == score_before + GRANARY_COST * REFUND_MULTIPLIER
        assert game.grid.special[5, 5] == SpecialType.NONE.value
        # pole je stále 1
        assert game.grid.cells[5, 5] == 1

    def test_cannot_remove_enemy_cell(self):
        game = make_game()
        game.grid.cells[5, 5] = 2  # hráč 2
        score_before = game.players[0].score
        game.remove_cell(5, 5)
        assert game.grid.cells[5, 5] == 2  # nezměnilo se
        assert game.players[0].score == score_before
    
    def test_cannot_remove_enemy_granary(self):
        game = make_game()
        game.grid.cells[5, 5] = 2  # hráč 2
        game.grid.special[5, 5] = SpecialType.GRANARY.value  
        score_before = game.players[0].score
        game.remove_cell(5, 5)
        assert game.grid.cells[5, 5] == 2  # nezměnilo se
        assert game.grid.special[5, 5] == SpecialType.GRANARY.value
        assert game.players[0].score == score_before

    def test_cannot_remove_mine(self):
        game = make_game()
        game.grid.special[5, 5] = SpecialType.MINE_INACTIVE.value  
        game.grid.special[6, 6] = SpecialType.MINE_ACTIVE.value  
        score_before = game.players[0].score
        game.remove_cell(5, 5)
        game.remove_cell(6, 6)

        assert game.grid.special[5, 5] == SpecialType.MINE_INACTIVE.value
        assert game.grid.special[6, 6] == SpecialType.MINE_ACTIVE.value

# speciální buňky
class TestSpecialCells:
    def test_granary_prevents_overpopulation(self):
        """Buňka chráněná sýpkou přežije přelidnění."""
        g = Grid(20, 20)
        # buňka [10,10] má 5 sousedů – normálně by zemřela
        g.cells[10, 10] = 1
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1)]:
            g.cells[10 + dr, 10 + dc] = 1
        # sýpka na sousední buňce stejného hráče
        g.cells[10, 11] = 1
        g.special[10, 11] = SpecialType.GRANARY.value
        g.next_generation(lambda r, c: 1, lambda *a: None)
        assert g.cells[10, 10] == 1

    def test_mine_activates_after_one_tick(self):
        """Neaktivní mina se po ticku aktivuje."""
        g = Grid(20, 20)
        g.special[10, 10] = SpecialType.MINE_INACTIVE.value
        g.next_generation(lambda r, c: 1, lambda *a: None)
        assert g.special[10, 10] == SpecialType.MINE_ACTIVE.value

    def test_mine_explodes_on_contact(self):
        """Aktivní mina zničí buňky v okolí."""
        g = Grid(20, 20)
        g.special[10, 10] = SpecialType.MINE_ACTIVE.value
        g.cells[10, 11] = 1
        #šlápla na minu
        g.cells[10, 10] = 1
        g.next_generation(lambda r, c: 1, mine_explosion)
        assert g.cells[10, 10] == 0
        assert g.cells[10, 11] == 0
        assert g.special[10, 10] == SpecialType.NONE.value
    
    def test_mine_does_not_destroy_flag(self):
        """Výbuch miny nezničí vlajku."""
        g = Grid(20, 20)
        g.special[10, 10] = SpecialType.MINE_ACTIVE.value
        g.special[10, 11] = SpecialType.FLAG.value
        g.cells[10, 10] = 1
        g.next_generation(lambda r, c: 1, mine_explosion)
        assert g.special[10, 11] == SpecialType.FLAG.value

    def test_factory_generates_income(self):
        """Továrna generuje příjem každý tick."""
        game = make_game()
        game.grid.cells[5, 5] = 1
        game.grid.special[5, 5] = SpecialType.FACTORY.value
        score_before = game.players[0].score
        game.collect_factory_income()
        assert game.players[0].score == score_before + FACTORY_INCOME

# test herních módů
class TestModes:
    def test_dominance_ends_at_max_ticks(self):
        game = make_game(ticks=20)
        game.phase = Phase.SIMULATING
        game.grid.cells[5, 5] = 1
        for _ in range(20):
            game.tick()
        assert game.phase == Phase.GAME_OVER
    def test_dominance_standings_sorted_by_cells(self):
        game = make_game(ticks=100)
        # hráč 1 má více buněk
        game.grid.cells[5, 5] = 1
        game.grid.cells[5, 6] = 1
        game.grid.cells[5, 7] = 1
        game.grid.cells[8, 8] = 2
        standings = game.mode.get_standings(game)
        assert standings[0]["player"].id == 1
        
    def test_elimination_detects_loser(self):
        game = make_game(num_players=2)
        game.mode = EliminationMode()
        game.phase = Phase.SIMULATING
        game.grid.cells[:] = 0
        game.grid.cells[5, 5] = 1  # jen hráč 1
        assert game.mode.check_winner(game) == True
        assert 2 in game.mode.elimination_order
 
    def test_elimination_winner_is_last(self):
        """Přeživší hráč je první ve standings."""
        game = make_game(num_players=2)
        game.mode = EliminationMode()
        game.grid.cells[:] = 0
        game.grid.cells[5, 5] = 1
        game.mode.check_winner(game)
        standings = game.mode.get_standings(game)
        assert standings[0]["player"].id == 1
 
    def test_flags_award_scores(self):
        game = make_game(num_players=2)
        game.mode = FlagsMode(max_ticks=100, num_flags=1)
        game.mode.place_flags(game.grid)
        fr, fc = game.mode.flag_positions[0]
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                r, c = fr + dr, fc + dc
                if 0 <= r < game.grid.height and 0 <= c < game.grid.width:
                    game.grid.cells[r, c] = 1
        game.mode.award_flag_scores(game)
        assert game.mode.flag_scores.get(1, 0) > 0
 
    def test_flags_standings_sorted_by_flag_score(self):
        """Standings jsou seřazeny podle flag_score."""
        game = make_game(num_players=2)
        game.mode = FlagsMode(max_ticks=100, num_flags=1)
        game.mode.flag_scores = {1: 10, 2: 5}
        standings = game.mode.get_standings(game)
        assert standings[0]["player"].id == 1
