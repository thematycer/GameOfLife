# player.py
from dataclasses import dataclass, field
from config import MAX_UPGRADE_LEVEL, UPGRADE_COST_BASE

@dataclass
class Player:
    id: int          # 1-based, odpovídá hodnotě v grid.cells
    name: str
    aggression: int = 0   # úroveň upgradu (0 = žádný)
    resilience: int = 0
    # mutace mi přišla jako špatná mechanika, jelikož jak drahé jsou budovy
    score: int = 0
    def upgrade_cost(self, upgrade: str) -> int:
        level = getattr(self, upgrade) # získej aktuální úroveň upgradu
        return UPGRADE_COST_BASE * (level + 1)

    def buy_upgrade(self, upgrade: str) -> bool:
        level = getattr(self, upgrade)
        if level >= MAX_UPGRADE_LEVEL:
            return False
        cost = self.upgrade_cost(upgrade)
        if self.score >= cost:
            self.score -= cost
            setattr(self, upgrade, level + 1)
            return True
        return False
    