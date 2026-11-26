from enum import Enum


IMAGE_SIZE = 810
CX, CY, PITCH = IMAGE_SIZE / 2, IMAGE_SIZE / 2, 42.6

SCORE_START_X = 110
SCORE_START_Y = 25
SCORE_WIDTH = 106
SCORE_HEIGHT = 38

class CellType(Enum):
    EMPTY = "empty"
    RED = "red"
    ORANGE = "orange"
    YELLOW = "yellow"
    GREEN = "green"
    BLUE = "blue"
    PURPLE = "purple"
    UNKNOWN = "unknown"

HUE_RANGES = {
    CellType.RED:    [(0, 7), (170, 179)],
    CellType.ORANGE: [(8, 25)],
    CellType.YELLOW: [(26, 34)],
    CellType.GREEN:  [(35, 84)],
    CellType.BLUE:   [(85, 129)],
    CellType.PURPLE: [(130, 169)],
}

CORNER_CELLS = {
    (0, 0):  CellType.RED,
    (0, 5):  CellType.GREEN,
    (5, 0):  CellType.PURPLE,
    (5, 10): CellType.BLUE,
    (10, 0): CellType.YELLOW,
    (10, 5): CellType.ORANGE,
}

COLOR_TO_CODE = {
    CellType.RED:    "R",
    CellType.GREEN:  "G",
    CellType.ORANGE: "O",
    CellType.BLUE:   "B",
    CellType.YELLOW: "Y",
    CellType.PURPLE: "P",
}


COLOR_ORDER = ["R", "G", "O", "B", "Y", "P"]

HEX_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, -1), (-1, 1)]

rows = [6, 7, 8, 9, 10, 11, 10, 9, 8, 7, 6]


CELL_COLORS = {
    CellType.RED:     (0, 0, 255),
    CellType.ORANGE:  (255, 165, 255),
    CellType.YELLOW:  (0, 255, 255),
    CellType.GREEN:   (0, 255, 0),
    CellType.BLUE:    (255, 0, 0),
    CellType.PURPLE:  (255, 0, 180),
    CellType.EMPTY:   (160, 160, 160),
    CellType.UNKNOWN: (255, 255, 255),
}