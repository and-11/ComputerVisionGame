import cv2 as cv
import numpy as np

from config import (
    CELL_COLORS,
    HUE_RANGES,
    SCORE_HEIGHT,
    SCORE_START_X,
    SCORE_START_Y,
    SCORE_WIDTH,
    COLOR_TO_CODE,
    COLOR_ORDER,
    CellType,
)
from helpers import extrage_careu, show_image


def draw_grid(image, start_x, start_y, width, height):
    vis = image.copy()
    for r in range(19):
        for c in range(6):
            x1 = start_x + c * width
            y1 = start_y + r * height
            x2 = x1 + width
            y2 = y1 + height
            cv.rectangle(vis, (x1, y1), (x2, y2), (0, 255, 0), 1)
    return vis

def set_grid():
    img = cv.imread("scor.jpg")
    warped = extrage_careu(img)

    win = "Grid"
    cv.namedWindow(win)
    cv.createTrackbar("start_x", win, 110, 400, lambda _: None)
    cv.createTrackbar("start_y", win, 25, 200, lambda _: None)
    cv.createTrackbar("width", win, 115, 200, lambda _: None)
    cv.createTrackbar("height", win, 40, 80, lambda _: None)

    while True:
        start_x = cv.getTrackbarPos("start_x", win)
        start_y = cv.getTrackbarPos("start_y", win)
        width = max(1, cv.getTrackbarPos("width", win))
        height = max(1, cv.getTrackbarPos("height", win))

        vis = draw_grid(warped, start_x, start_y, width, height)
        cv.imshow(win, vis)

        if cv.waitKey(30) & 0xFF in (27, ord("q")):
            break

    cv.destroyAllWindows()
    print(f"start_x = {start_x}, start_y = {start_y}, width = {width}, height = {height}")

def classify_score_patch(patch):
    hsv = cv.cvtColor(patch, cv.COLOR_BGR2HSV)
    med_h, med_s, med_v = np.median(hsv, axis=(0, 1))

    if med_s < 60 or med_v < 85:
        return CellType.EMPTY

    hue = int(round(med_h)) % 180
    for cell_type, ranges in HUE_RANGES.items():
        if any(lo <= hue <= hi for lo, hi in ranges):
            return cell_type

    return CellType.UNKNOWN

CODE_TO_CELL = {code: cell_type for cell_type, code in COLOR_TO_CODE.items()}


def get_scoreboard(
    image,
    start_x=SCORE_START_X,
    start_y=SCORE_START_Y,
    width=SCORE_WIDTH,
    height=SCORE_HEIGHT,
):
    vis = image.copy()
    state = []

    for c, code in enumerate(COLOR_ORDER):
        expected_color = CODE_TO_CELL[code]
        best_r = 18
        best_pixels = -1

        for r in range(19):
            x1 = start_x + c * width
            y1 = start_y + r * height
            patch = image[y1 : y1 + height, x1 : x1 + width]

            hsv = cv.cvtColor(patch, cv.COLOR_BGR2HSV)
            h, s, v = cv.split(hsv)

            if expected_color == CellType.BLUE:
                mask = (s > 100) & (v > 100)
            else:
                hue_mask = np.zeros_like(h, dtype=bool)
                for lo, hi in HUE_RANGES[expected_color]:
                    hue_mask |= (h >= lo) & (h <= hi)
                mask = hue_mask & (s > 80) & (v > 80)

            pixels = int(mask.sum())
            if pixels > best_pixels:
                best_pixels = pixels
                best_r = r

        x1 = start_x + c * width
        y1 = start_y + best_r * height
        cv.rectangle(vis, (x1, y1), (x1 + width, y1 + height), CELL_COLORS[expected_color], 3)
        state.append(18 - best_r)

    # show_image("Scoreboard", vis)

    return state



if __name__ == "__main__":
    img = cv.imread("faulty.jpg")
    warped = extrage_careu(img)
    vis = get_scoreboard(warped)


