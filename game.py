''' 
řeší hlavní herní logiku. Propojuje hráče, mřížku a ui.
'''
from enum import Enum
from grid import Grid
from config import CELL_COST, FACTORY_COST, FACTORY_INCOME, GRANARY_COST, GRANARY_UNKEEP_COST,  MINE_COST, PANEL_WIDTH, REFUND_MULTIPLIER
from player import Player
import numpy as np
from special import SpecialType, mine_explosion
from modes import FlagsMode, GameMode


class Phase(Enum):
    SET_UP = 1
    SIMULATING = 2
    ACTION_PHASE = 3
    GAME_OVER = 4

class Game:
    def __init__(self, num_players, action_interval, mode, start_score=100, player_names=None, random_start=True, window_width=800, window_height=600, cell_size=10):
        self.num_players = num_players
        
        self.current_player = 0      # index hráče na tahu (0 = hráč 1)
        self.tick_count = 0
        self.action_interval = action_interval
        self.mode = mode  # herní mód
        self.standings = []  # seznam hráčů seřazený podle skóre (pro UI)
        
        self.window_width = window_width
        self.window_height = window_height
        self.cell_size = cell_size

        grid_w = (self.window_width - PANEL_WIDTH) // self.cell_size
        grid_h = self.window_height // self.cell_size

        names = player_names or [f"Hráč {i+1}" for i in range(num_players)]
        self.players = [
            Player(id=i+1, name=names[i], score=start_score)
            for i in range(num_players)
        ]
        self.grid = Grid(grid_w, grid_h)

        if random_start:
            self.grid.randomize(num_players=num_players)
        
        if isinstance(self.mode, FlagsMode):
            self.mode.place_flags(self.grid)
        
        self.phase = Phase.ACTION_PHASE 
        
        




    def current_player_obj(self) -> Player:
        return self.players[self.current_player]# vrátí objekt hráče, který je na tahu
    
    def tick(self):
        # posune simulaci o jeden krok, pokud není fáze akce
        if self.phase != Phase.SIMULATING:
            return
        self.grid.next_generation(self.dominant_neighbor, mine_explosion)
        self.collect_factory_income()
        self.tick_count += 1
        if isinstance(self.mode, FlagsMode):
            self.mode.award_flag_scores(self)

        if self.tick_count % self.action_interval == 0:
            self.calculate_scores()
            self.phase = Phase.ACTION_PHASE
            if self.mode.check_winner(self):
                self.standings = self.mode.get_standings(self)
                self.phase = Phase.GAME_OVER

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
        player = self.current_player_obj()
        if special_type == SpecialType.GRANARY:
            if self.grid.cells[row, col] != self.current_player + 1: # jen na vlastní buňku
                return
            if self.grid.special[row, col] == SpecialType.GRANARY.value:
                return  # již je zde sýpka
            if self.grid.special[row, col] != SpecialType.NONE.value:
                return  # nelze umístit jiný speciální typ
            if player.score < GRANARY_COST:
                return  # nedostatek bodů
            player.score -= GRANARY_COST
            self.grid.special[row, col] = special_type.value
        elif special_type == SpecialType.MINE_INACTIVE:
            if self.grid.cells[row, col] != 0:  # jen na prázdné pole
                return
            if self.grid.special[row, col] != SpecialType.NONE.value:
                return  # nelze umístit jiný speciální typ
            if player.score < MINE_COST:
                return  # nedostatek bodů
            player.score -= MINE_COST
            self.grid.special[row, col] = SpecialType.MINE_INACTIVE.value
        elif special_type == SpecialType.FACTORY:
            if self.grid.cells[row, col] != self.current_player + 1:
                return
            if self.grid.special[row, col] != SpecialType.NONE.value:
                return
            if player.score < FACTORY_COST:
                return
            player.score -= FACTORY_COST
            self.grid.special[row, col] = SpecialType.FACTORY.value

    
    def calculate_scores(self):
        # spočítá skóre hráčů na základě počtu jejich buněk a zaplatí údržby za speciální typy
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

    def collect_factory_income(self):
        for player in self.players:
            factory_mask = (self.grid.special == SpecialType.FACTORY.value) & (self.grid.cells == player.id)
            count = int(np.sum(factory_mask))
            player.score += count * FACTORY_INCOME
        


    def dominant_neighbor(self, row: int, col: int) -> int:
        # vrací ID hráče, který má převahu nad danou pozicí a tedy by jí měl dostat

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
        