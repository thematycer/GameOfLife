''' 
Konfigurační soubor pro hru Game of Life
Využívá se pro nastavení konstant ve hře.
'''
PANEL_WIDTH = 200  # šířka panelu pro ovládací prvky
#používá se jen pro okno před set upem
WINDOW_WIDTH = 800 + PANEL_WIDTH 
WINDOW_HEIGHT = 600
CELL_SIZE = 10  # pixelů na buňku

# kolik hráč dostane zpátky za prodej buňky. 0.5 = 50% zpátky.
REFUND_MULTIPLIER = 0.5  # hráč dostane zpět 50% skóre za odstranění buňky

# ceny během fáze akce
CELL_COST = 10
#cena za upgrade buňky, cena se zvyšuje s každým upgradem
UPGRADE_COST_BASE = 50
MAX_UPGRADE_LEVEL = 18# větší by mohl rozbít nějaké funkce

GRANARY_COST = 100
GRANARY_UNKEEP_COST = 25 # cena za údržbu sýpky, odečítá se z hráčova skóre na konci fáze simulace


MINE_COST = 50
MINE_RADIUS = 1  # poloměr exploze v buňkách (1 = 3×3 oblast)

FACTORY_COST = 150
FACTORY_INCOME = 5 # příjem za tick


FPS = 10  # rychlost simulace

COLOR_BACKGROUND = (15, 15, 15)
PLAYER_COLORS = [
    COLOR_BACKGROUND,  # 0 = mrtvá buňka (černá)
    (255, 0, 0),    #1 hráč - červená
    (0, 255, 0),    #2 hráč - zelená
    (0, 0, 255),    #3 hráč - modrá
    (255, 255, 0),  #4 hráč - žlutá
    (255, 165, 0),  #5 hráč - oranžová
    (128, 0, 128),  #6 hráč - fialová
]
COLOR_GRID = (30, 30, 30)