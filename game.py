from enum import Enum

from grid import Grid
from config import CELL_COST, GRANARY_COST, GRANARY_UNKEEP_COST, GRID_WIDTH, GRID_HEIGHT, REFUND_MULTIPLIER
from player import Player
import numpy as np
from special import SpecialType


class Phase(Enum):
    SIMULATING = 1
    ACTION_PHASE = 2

class Game:
    def __init__(self, num_players: int, action_interval: int):
        self.players = [Player(id=i+1, name=f"Hráč {i+1}") for i in range(num_players)]
        self.grid = Grid(GRID_WIDTH, GRID_HEIGHT)
        self.grid.randomize(num_players=num_players)
        
        self.num_players = num_players
        self.current_player = 0      # index hráče na tahu (0 = hráč 1)
        self.tick_count = 0
        self.action_interval = action_interval
        self.phase = Phase.SIMULATING


    def current_player_obj(self) -> Player:
        return self.players[self.current_player]# vrátí objekt hráče, který je na tahu
    
    def tick(self):
        # posune simulaci o jeden krok, pokud není fáze akce
        if self.phase != Phase.SIMULATING:
            return
        self.grid.next_generation(self.dominant_neighbor)
        self.tick_count += 1
        if self.tick_count % self.action_interval == 0:
            self.calculate_scores()
            self.phase = Phase.ACTION_PHASE

    def confirm_action(self):
        # hráč stiskl Enter – předej tah dalšímu hráči
        if self.phase != Phase.ACTION_PHASE:
            return
        self.current_player = (self.current_player + 1) % self.num_players
        if self.current_player == 0:
            # všichni hráči odehráli svůj tah, pokračuj v simulaci
            self.phase = Phase.SIMULATING

    def place_cell(self, row: int, col: int):
        # umístí buňku aktuálního hráče během fáze akce
        if self.phase != Phase.ACTION_PHASE:
            return
        if self.grid.cells[row, col] != 0:  # toto místo je již obsazeno
            return 
        player = self.current_player_obj()
        if player.score < CELL_COST:  # hráč nemá dostatek bodů na umístění buňky
            return
        player.score -= CELL_COST     # odečti cenu buňky
        self.grid.cells[row, col] = player.id
    
    def place_special(self, row, col, special_type):
        if self.phase != Phase.ACTION_PHASE:
            return
        if self.grid.cells[row, col] != self.current_player + 1: # hráč může umístit speciální buňku jen na vlastní buňku
            return
        player = self.current_player_obj()
        if special_type == SpecialType.GRANARY:
            if self.grid.special[row, col] == SpecialType.GRANARY.value:
                return  # již je zde sýpka
            if player.score < GRANARY_COST:
                return  # nedostatek bodů
            player.score -= GRANARY_COST
            self.grid.special[row, col] = special_type.value

    
    def calculate_scores(self):
        for player in self.players:
            player.score += int(np.sum(self.grid.cells == player.id))
        self.pay_upkeep_for_granaries()
    
    def pay_upkeep_for_granaries(self):
        for player in self.players:
            granary_mask = (self.grid.special == SpecialType.GRANARY.value) & (self.grid.cells == player.id)
            granary_count = int(np.sum(granary_mask))
            upkeep_cost = granary_count * GRANARY_UNKEEP_COST
            
            if player.score < upkeep_cost:
                # hráč nemá dostatek bodů na údržbu sýpek, ztrácí všechny své sýpky
                self.grid.special[self.grid.cells == player.id] = 0
                player.score = 0
            else:
                player.score -= upkeep_cost

    def dominant_neighbor(self, row: int, col: int) -> int:
        # spočítej kolik sousedů má každý hráč
        counts = {}  # {player_id: počet}
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r == row and c == col) or r < 0 or c < 0 or r >= self.grid.height or c >= self.grid.width:
                    continue 
                owner = self.grid.cells[r, c]
                if owner != 0:
                    player = self.players[owner - 1]
                    bonus = 1+player.aggression * 0.5 # 1 + 0.5 za každý bod agrese
                    counts[owner] = counts.get(owner, 0) + bonus
        if not counts:
            return 0
        return max(counts, key=lambda p: counts[p])
    
    def remove_cell(self, row: int, col: int):
        if self.phase != Phase.ACTION_PHASE:
            return
        # hráč může odstranit jen vlastní buňky
        if self.grid.cells[row, col] != self.current_player + 1:
            return
        player = self.current_player_obj()

        if self.grid.special[row, col] == SpecialType.GRANARY.value:
            player.score += GRANARY_COST*REFUND_MULTIPLIER
            self.grid.special[row, col] = SpecialType.NONE.value
        elif self.grid.special[row, col] == SpecialType.NONE.value:
            player.score += CELL_COST*REFUND_MULTIPLIER
            self.grid.cells[row, col] = 0
        