# řeší mřížku (2D pole) a její logiku
import numpy as np
from special import SpecialType, granary_effect
class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # inicializace mřížky s nulami (všechny buňky mrtvé)
        self.cells = np.zeros((height, width), dtype=int)
        # iniciace mřížky s peciálními buňkami
        self.special = np.zeros((height, width), dtype=int)

    def randomize(self, density: float = 0.3, num_players: int = 1):
        self.cells = np.random.choice(
            range(num_players + 1),  # 0 = mrtvá, 1..n = hráči
            size=(self.height, self.width),
            p=[1 - density] + [density / num_players] * num_players
        )

    def count_neighbors(self, row: int, col: int) -> int:
        count = 0
        # procházej sousední buňky
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r == row and c == col) or r < 0 or c < 0 or r >= self.height or c >= self.width:
                    continue #ignoruj buňku sama sebe a buňky mimo mřížku
                if self.cells[r, c] > 0:  
                    count += 1
        return count

    def next_generation(self, dominant_neighbor_func):
        #vytvoř prázdnou kopii mřížky pro novou generaci. Chceme zachovat původní mřížku pro zkoumání pravidel.
        new_cells = np.zeros_like(self.cells)
        new_special = np.zeros_like(self.special)
        for row in range(self.height):
            for col in range(self.width):
                neighbors = self.count_neighbors(row, col)
                alive = self.cells[row, col] > 0
                protected = granary_effect(self, row, col)  # zkontroluj, zda je buňka chráněna sýpkou
                if (alive and neighbors in (2, 3)) or protected:
                    # buňka je živá a má 2 nebo 3 sousedy, zůstává živá
                    new_cells[row, col] = self.cells[row, col]
                    new_special[row, col] = self.special[row, col]
                elif not alive and neighbors == 3:
                    # buňka je mrtvá a má přesně 3 sousedy, stává se živou
                    new_cells[row, col] = dominant_neighbor_func(row, col)
                # else: buňka zůstává mrtvá (0). Řeší jak přelidnění, tak osamělosti
        self.cells = new_cells
        self.special = new_special