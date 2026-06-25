# player.py
from dataclasses import dataclass, field
from config import UPGRADE_COST_BASE

@dataclass
class Player:
    id: int          # 1-based, odpovídá hodnotě v grid.cells
    name: str
    aggression: int = 0   # úroveň upgradu (0 = žádný)
    resilience: int = 0
    score: int = 0
    def upgrade_cost(self, upgrade: str) -> int:
        level = getattr(self, upgrade) # získej aktuální úroveň upgradu
        return UPGRADE_COST_BASE * (level + 1)

    def buy_upgrade(self, upgrade: str) -> bool:
        cost = self.upgrade_cost(upgrade)
        if self.score >= cost:
            self.score -= cost
            setattr(self, upgrade, getattr(self, upgrade) + 1)
            return True
        return False
    