# řeší mřížku (2D pole) a její logiku
from networkx import density
import numpy as np
class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        # inicializace mřížky s nulami (všechny buňky mrtvé)
        self.cells = np.zeros((height, width), dtype=int)

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

    def dominant_neighbor(self, row: int, col: int) -> int:
        # spočítej kolik sousedů má každý hráč
        counts = {}  # {player_id: počet}
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r == row and c == col) or r < 0 or c < 0 or r >= self.height or c >= self.width:
                    continue 
                owner = self.cells[r, c] # zjisti, kdo vlastní buňku
                if owner != 0:  # 0 = mrtvá, tedy ignoruj
                    counts[owner] = counts.get(owner, 0) + 1
        if not counts:
            return 0  # pokud žádní sousedé nejsou živí, vrať 0, nemělo by se stát, ale pro jistotu
        return max(counts, key=lambda p: counts[p])
        # při remíze max() vrátí toho s nižším ID – to je v pořádku

    def next_generation(self):
        #vytvoř prázdnou kopii mřížky pro novou generaci. Chceme zachovat původní mřížku pro zkoumání pravidel.
        new_cells = np.zeros_like(self.cells)
        for row in range(self.height):
            for col in range(self.width):
                neighbors = self.count_neighbors(row, col)
                alive = self.cells[row, col] > 0
                
                if alive and neighbors in (2, 3):
                    # buňka je živá a má 2 nebo 3 sousedy, zůstává živá
                    new_cells[row, col] = self.cells[row, col]
                elif not alive and neighbors == 3:
                    # buňka je mrtvá a má přesně 3 sousedy, stává se živou
                    new_cells[row, col] = self.dominant_neighbor(row, col)
                # else: buňka zůstává mrtvá (0). Řeší jak přelidnění, tak osamělosti
        self.cells = new_cells 