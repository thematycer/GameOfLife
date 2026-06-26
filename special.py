from enum import Enum

from config import MINE_RADIUS

class SpecialType(Enum):
    NONE = 0
    GRANARY = 1
    MINE_INACTIVE = 2  # první kolo po umístění
    MINE_ACTIVE = 3    # od druhého kola, exploduje při kontaktu
    FLAG = 4 # Vlajky pro zabrání

def granary_effect(grid, row: int, col: int) -> bool:
    """
    Vrátí True pokud je buňka na [row, col] chráněna sýpkou stejného hráče.
    Buňka je chráněna sýpkou, pokud má v okolí alespoň jednu sýpku.
    """
    owner = grid.cells[row, col]
    for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r == row and c == col) or r < 0 or c < 0 or r >= grid.height or c >= grid.width:
                    continue #ignoruj buňku sama sebe a buňky mimo mřížku
                if grid.special[r, c] == SpecialType.GRANARY.value and grid.cells[r, c] == owner:
                    return True
    return False

def mine_explosion(cells, special, row: int, col: int, height: int, width: int):
    for r in range(row - MINE_RADIUS, row + MINE_RADIUS + 1):
        for c in range(col - MINE_RADIUS, col + MINE_RADIUS + 1):
            if r < 0 or c < 0 or r >= height or c >= width:
                continue
            if special[r, c] == SpecialType.FLAG.value:
                continue
            cells[r, c] = 0
            special[r, c] = SpecialType.NONE.value