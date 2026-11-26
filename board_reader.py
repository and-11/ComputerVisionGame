import cv2 as cv
import numpy as np

from config import CORNER_CELLS, CX, CY, HUE_RANGES, PITCH, rows, CellType, CELL_COLORS
from helpers import show_image, extrage_careu, get_cell_center


def extract_cells(image, cx=CX, cy=CY, pitch=PITCH, scale=0.8):
    dy = pitch * np.sqrt(3) / 2
    half = int(pitch * scale / 2)

    board_patches = []
    for r, n in enumerate(rows):
        y = int(round(cy + (r - 5) * dy))
        x0 = cx - (n - 1) * pitch / 2
        row_patches = []

        for k in range(n):
            x = int(round(x0 + k * pitch))
            patch = image[y - half : y + half, x - half : x + half].copy()
            row_patches.append(patch)

        board_patches.append(row_patches)

    return board_patches



def classify_patch(patch, empty_v_thr=135):
    hsv = cv.cvtColor(patch, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(hsv)

    # dark_frac = float((v < 75).mean())
    # if dark_frac < dark_frac_thr:
    #     return CellType.EMPTY

    if np.median(v) > empty_v_thr:
        return CellType.EMPTY

    # symbol = (v >= 100) & (s >= 65)
    # symbol = (v >= 100) & (s >= 55)
    symbol = (v >= 120) & (s >= 65)
    # symbol = (v >= 70) & (s >= 35)
    if symbol.sum() < 10:
        return CellType.UNKNOWN

    hs = h[symbol]
    ss = s[symbol].astype(float)

    hist = np.bincount(hs, weights=ss, minlength=180)
    padded = np.r_[hist[-3:], hist, hist[:3]]
    hue = int(np.argmax(np.convolve(padded, np.ones(7) / 7, mode="valid")))

    for cell_type, ranges in HUE_RANGES.items():
        if any(lo <= hue <= hi for lo, hi in ranges):
            return cell_type
        
    return CellType.UNKNOWN



def visualize_patches(image, board_patches, cx=CX, cy=CY, pitch=PITCH, scale=0.8):
    half = int(pitch * scale / 2)
    vis = image.copy()

    for r, row_patches in enumerate(board_patches):
        for k, patch in enumerate(row_patches):
            x, y = get_cell_center(r, k, cx=cx, cy=cy, pitch=pitch)
            cell_type = classify_patch(patch)
            color = CELL_COLORS[cell_type]
            thickness = 1 if cell_type == CellType.EMPTY else 2

            cv.rectangle(vis, (x - half, y - half), (x + half, y + half), color, thickness)

    for r, k in [(1, 0), (1, 5), (5, 10)]:
        v = cv.cvtColor(patches[r][k], cv.COLOR_BGR2HSV)[:, :, 2]
        print(f"({r}, {k}) dark_frac: {(v < 75).mean():.3f}")

    return vis











# pt a vedea ce pixeli sunt luati in considerare, ca initial luam prea mult din fundal
def get_considered_pixels(image, board_patches, cx=CX, cy=CY, pitch=PITCH, scale=0.8, empty_v_thr=135):
    half = int(pitch * scale / 2)
    canvas = np.zeros_like(image)

    for r, row_patches in enumerate(board_patches):
        for k, patch in enumerate(row_patches):
            hsv = cv.cvtColor(patch, cv.COLOR_BGR2HSV)
            _, s, v = cv.split(hsv)

            if np.median(v) > empty_v_thr:
                continue

            symbol = (v >= 120) & (s >= 65)
            if symbol.sum() < 10:
                continue

            x, y = get_cell_center(r, k, cx=cx, cy=cy, pitch=pitch)
            canvas[y - half : y + half, x - half : x + half][symbol] = patch[symbol]

    return canvas





if __name__ == '__main__':

    # img = cv.imread("exemplu.jpg")
    # img = extrage_careu(img)

    # patches = extract_cells(img)

    # cv.imwrite('read.jpg', visualize_patches(img, patches))
    # cv.imwrite("considered_pixels.jpg", get_considered_pixels(img, patches))


    