from enum import Enum

class SpecialType(Enum):
    NONE = 0
    GRANARY = 1

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