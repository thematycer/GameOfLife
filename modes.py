# modes.py
from abc import ABC, abstractmethod
import numpy as np

from special import SpecialType

#abstraktní třída pro herní módy
class GameMode(ABC):
    @abstractmethod
    def check_winner(self, game) -> int | None:
        """Vrátí ID vítěze, nebo None pokud hra pokračuje."""
        pass

    def get_standings(self, game) -> list[dict]:
        """Vrátí seřazený seznam hráčů s výsledky."""
        pass

    @abstractmethod
    def description(self) -> str:
        """Krátký popis módu pro UI."""
        pass

class DominanceMode(GameMode):
    # hráč s nejvíce buňkami po max_ticks vyhrává
    def __init__(self, max_ticks: int):
        self.max_ticks = max_ticks

    def check_winner(self, game) -> bool:
        return game.tick_count >= self.max_ticks

    def get_standings(self, game) -> list[dict]:
        results = []
        for player in game.players:
            cell_count = int(np.sum(game.grid.cells == player.id))
            results.append({
                "player": player,
                "cells": cell_count,
                "score": player.score,
            })
        # seřaď podle počtu buněk
        return sorted(results, key=lambda r: r["cells"], reverse=True)

    def description(self) -> str:
        return f"Dominance – nejvíce buněk po {self.max_ticks} ticích"
    
class EliminationMode(GameMode):
    #poslední přeživší vyhrává
    def __init__(self):
        self.elimination_order = []  # seznam ID hráčů v pořadí vyřazení

    def check_winner(self, game) -> bool:
        # zkontroluj kteří hráči jsou ještě živí
        for player in game.players:
            if player.id in self.elimination_order:
                continue  # už vyřazen
            cell_count = int(np.sum(game.grid.cells == player.id))
            if cell_count == 0:
                player.score = 0
                self.elimination_order.append(player.id)

        # hra končí když zbývá jen jeden hráč
        alive = [p for p in game.players if p.id not in self.elimination_order]
        if len(alive) <= 1:
            # přidej posledního přeživšího
            if alive and alive[0].id not in self.elimination_order:
                self.elimination_order.append(alive[0].id)
            return True
        return False

    def get_standings(self, game) -> list[dict]:
        # přeživší je první – tedy obráceně
        results = []
        for player_id in reversed(self.elimination_order):
            player = next(p for p in game.players if p.id == player_id)
            results.append({
                "player": player,
                "cells": int(np.sum(game.grid.cells == player.id)),
                "score": player.score,
            })
        return results

    def description(self) -> str:
        return "Eliminace – poslední přeživší vítězí"

class FlagsMode(GameMode):
    def __init__(self, max_ticks: int, num_flags: int = 5, flag_radius: int = 2):
        self.max_ticks = max_ticks
        self.num_flags = num_flags
        self.flag_radius = flag_radius
        self.flag_positions = []   # [(row, col), ...]
        self.flag_scores = {}      # {player_id: body za vlajky}

    def place_flags(self, grid):
        """Náhodně rozmístí vlajky – volá se po inicializaci gridu."""
        import random
        self.flag_positions = []
        for _ in range(self.num_flags):
            r = random.randint(2, grid.height - 3)
            c = random.randint(2, grid.width - 3)
            self.flag_positions.append((r, c))
            grid.special[r, c] = SpecialType.FLAG.value

    def award_flag_scores(self, game):
        """Udělí body za ovládané vlajky – volá se každý tick."""
        for (fr, fc) in self.flag_positions:
            counts = {}
            for r in range(fr - self.flag_radius, fr + self.flag_radius + 1):
                for c in range(fc - self.flag_radius, fc + self.flag_radius + 1):
                    if 0 <= r < game.grid.height and 0 <= c < game.grid.width:
                        owner = game.grid.cells[r, c]
                        if owner != 0:
                            counts[owner] = counts.get(owner, 0) + 1
            if counts:
                dominant = max(counts, key=lambda p: counts[p])
                self.flag_scores[dominant] = self.flag_scores.get(dominant, 0) + 1

    def check_winner(self, game) -> bool:
        return game.tick_count >= self.max_ticks

    def get_standings(self, game) -> list[dict]:
        results = []
        for player in game.players:
            results.append({
                "player": player,
                "cells": int(np.sum(game.grid.cells == player.id)),
                "score": player.score,
                "flag_score": self.flag_scores.get(player.id, 0),
            })
        return sorted(results, key=lambda r: r["flag_score"], reverse=True)

    def description(self) -> str:
        return f"Vlajky – nejvíce bodů za zóny po {self.max_ticks} ticích"