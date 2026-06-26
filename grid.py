# řeší mřížku (2D pole) a její logiku
''' 
Řeší logiku mříky za využití dvou 2d polý.
cells - určuje vlastníka
special - typ speciální budovy na daném poly
''' 
import random
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
        # náhodně rozdělií buňky mezi hráče
        # density říká jaký je poměr živých buněk k mrtvým (0.3 = 30% živých)
        self.cells = np.random.choice(
            range(num_players + 1),  # 0 = mrtvá, 1..n = hráči
            size=(self.height, self.width),
            p=[1 - density] + [density / num_players] * num_players
        )

    def count_neighbors(self, row: int, col: int) -> int:
        # Počítá živé sousedy v okolí 3×3 (bez středu).
        # Buňky mimo mřížku se považují za mrtvé.
        count = 0
        # procházej sousední buňky
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r == row and c == col) or r < 0 or c < 0 or r >= self.height or c >= self.width:
                    continue #ignoruj buňku sama sebe a buňky mimo mřížku
                if self.cells[r, c] > 0:  
                    count += 1
        return count

    def next_generation(self, dominant_neighbor_func, mine_explosion_func):
        # aplukuje pravidla hry na celou  mřížku

        # 1. nejdřív vytvoř nové mřížky
        new_cells = np.zeros_like(self.cells)
        new_special = np.zeros_like(self.special)

        # 2. aplikuj pravidla GoL
        for row in range(self.height):
            for col in range(self.width):
                neighbors = self.count_neighbors(row, col)
                alive = self.cells[row, col] > 0
                protected = granary_effect(self, row, col)
                survives = alive and (neighbors in (2, 3) or (protected and neighbors > 3))
                if alive and not survives:
                    owner = self.cells[row, col]
                    player = players[owner - 1]
                    chance = min(player.resilience * 0.05, 0.90)  # max 90%, level 18
                    if random.random() < chance:
                        survives = True
                
                if survives:
                    new_cells[row, col] = self.cells[row, col]
                    new_special[row, col] = self.special[row, col]
                elif not alive and neighbors == 3:
                    new_cells[row, col] = dominant_neighbor_func(row, col)
                
                # speciální typ co nepotřebuje vlasníka
                if not alive and self.special[row, col] in (SpecialType.MINE_INACTIVE.value,SpecialType.MINE_ACTIVE.value, SpecialType.FLAG.value):
                    new_special[row, col] = self.special[row, col]


        # 3. zpracuj miny na new_cells/new_special
        # nejdřív si je uložíme, aby výbuch nemohl vymazat minu, která by také chtěla vybuchnout
        mines_to_explode = []
        for row in range(self.height):
            for col in range(self.width):
                s = new_special[row, col]
                cell = new_cells[row, col]
                if s == SpecialType.MINE_INACTIVE.value and cell > 0:
                    new_special[row, col] = SpecialType.NONE.value   # deaktivace
                elif s == SpecialType.MINE_INACTIVE.value:
                    new_special[row, col] = SpecialType.MINE_ACTIVE.value  # aktivuj
                elif s == SpecialType.MINE_ACTIVE.value and cell > 0:
                    mines_to_explode.append((row, col))  # naplánuj výbuch

        # 4. aplikuj výbuchy až po iteraci
        for (r, c) in mines_to_explode:
            mine_explosion_func(new_cells, new_special, r, c, self.height, self.width)

        self.cells = new_cells
        self.special = new_special