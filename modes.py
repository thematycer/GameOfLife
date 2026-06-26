# modes.py
from abc import ABC, abstractmethod
import numpy as np

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