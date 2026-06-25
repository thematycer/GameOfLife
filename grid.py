# řeší mřížku (2D pole) a její logiku
import numpy as np
class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # inicializace mřížky s nulami (všechny buňky mrtvé)
        self.cells = np.zeros((height, width), dtype=int)

    def randomize(self, density: float = 0.3):
        # náhodně nastav buňky na živé (1) s danou hustotou
        self.cells = np.random.choice([0, 1], size=(self.height, self.width), p=[1 - density, density])

    def count_neighbors(self, row: int, col: int) -> int:
        count = 0
        # procházej sousední buňky
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r == row and c == col) or r < 0 or c < 0 or r >= self.height or c >= self.width:
                    continue #ignoruj buňku sama sebe a buňky mimo mřížku
                count += self.cells[r, c]
        return count

    def next_generation(self):
        #vytvoř prázdnou kopii mřížky pro novou generaci. Chceme zachovat původní mřížku pro zkoumání pravidel.
        new_cells = np.zeros_like(self.cells)
        for row in range(self.height):
            for col in range(self.width):
                neighbors = self.count_neighbors(row, col)
                alive = self.cells[row, col] == 1
                
                if alive and neighbors in (2, 3):
                    # buňka je živá a má 2 nebo 3 sousedy, zůstává živá
                    new_cells[row, col] = 1
                elif not alive and neighbors == 3:
                    # buňka je mrtvá a má přesně 3 sousedy, stává se živou
                    new_cells[row, col] = 1
                # else: buňka zůstává mrtvá (0). Řeší jak přelidnění, tak osamělosti
        self.cells = new_cells 