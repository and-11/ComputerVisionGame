from enum import Enum


IMAGE_SIZE = 810
CX, CY, PITCH = IMAGE_SIZE / 2, IMAGE_SIZE / 2, 42.6


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

CORNER_CELLS = {(0, 0), (0, 5), (5, 0), (5, 10), (10, 0), (10, 5)}

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