# Konfigurační soubor pro hru Game of Life
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

CELL_SIZE = 10  # pixelů na buňku

GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

FPS = 10  # počet ticků za sekundu

COLOR_BACKGROUND = (15, 15, 15)
PLAYER_COLORS = [
    (255, 0, 0),    #1 hráč - červená
    (0, 255, 0),    #2 hráč - zelená
    (0, 0, 255),    #3 hráč - modrá
    (255, 255, 0),  #4 hráč - žlutá
    (255, 165, 0),  #5 hráč - oranžová
    (128, 0, 128),  #6 hráč - fialová
]
COLOR_GRID = (30, 30, 30)