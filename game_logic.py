import os
import cv2 as cv

from config import CORNER_CELLS, COLOR_TO_CODE, COLOR_ORDER, rows, CellType, HEX_DIRECTIONS
from helpers import extrage_careu
from board_reader import extract_cells, classify_patch


def _build_position_maps():
    rc_to_pos_map = {}
    pos_to_rc_map = {}
    pos = 1
    for r, n in enumerate(rows):
        for k in range(n):
            if (r, k) not in CORNER_CELLS:
                rc_to_pos_map[(r, k)] = pos
                pos_to_rc_map[pos] = (r, k)
                pos += 1
    return rc_to_pos_map, pos_to_rc_map


RC_TO_POS, POS_TO_RC = _build_position_maps()


def rc_to_pos(row, col):
    if (row, col) not in RC_TO_POS:
        raise ValueError(f"Cell ({row}, {col}) is a printed corner or out of bounds.")
    return RC_TO_POS[(row, col)]


def pos_to_rc(pos):
    if pos not in POS_TO_RC:
        raise ValueError(f"Position {pos} is out of bounds.")
    return POS_TO_RC[pos]


def rc_to_axial(row, col):
    return col - min(row, 5), row


def axial_to_rc(q, r):
    if r < 0 or r >= len(rows):
        return None
    col = q + min(r, 5)
    if col < 0 or col >= rows[r]:
        return None
    return r, col



def create_initial_board():
    board = [[CellType.EMPTY for _ in range(n)] for n in rows]
    for (r, k), cell_type in CORNER_CELLS.items():
        board[r][k] = cell_type
    return board


def print_board(board):
    max_len = max(rows)
    for row in board:
        indent = " " * (max_len - len(row))
        cells = " ".join(
            "." if c == CellType.EMPTY else COLOR_TO_CODE.get(c, "?")
            for c in row
        )
        print(f"{indent}{cells}")


def read_board_from_image(image_path):
    img = cv.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    board_img = extrage_careu(img)
    patches = extract_cells(board_img)
    board = [[classify_patch(patch) for patch in row] for row in patches]

    for (r, k), cell_type in CORNER_CELLS.items():
        board[r][k] = cell_type

    return board

def get_move(prev_board, curr_board):
    move = []
    for r, n in enumerate(rows):
        for k in range(n):
            if (r, k) in CORNER_CELLS:
                continue
            if prev_board[r][k] == CellType.EMPTY and curr_board[r][k] in COLOR_TO_CODE:
                move.append((rc_to_pos(r, k), COLOR_TO_CODE[curr_board[r][k]]))

    move.sort(key=lambda item: item[0])
    return move




def calculate_score(prev_board, move):
    points = {code: 0 for code in COLOR_ORDER}

    for pos, color_code in move:
        row, col = pos_to_rc(pos)
        q0, r0 = rc_to_axial(row, col)

        for dq, dr in HEX_DIRECTIONS:
            step = 1
            while True:
                neighbor = axial_to_rc(q0 + dq * step, r0 + dr * step)
                if neighbor is None:
                    break
                nr, nk = neighbor
                if COLOR_TO_CODE.get(prev_board[nr][nk]) == color_code:
                    points[color_code] += 1
                    step += 1
                else:
                    break

    parts = [f"{points[c]}{c}" for c in COLOR_ORDER if points[c] > 0]
    return " ".join(parts) if parts else "0"




def write_move_file(output_path, move, score=0):
    lines = [f"{pos} {color}" for pos, color in move]
    lines.append(str(score))
    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")

def run_game(directory, output_directory):
    image_files = sorted(
        f for f in os.listdir(directory) if f.lower().endswith(".jpg")
    )

    prev_board = create_initial_board()

    for step, filename in enumerate(image_files, start=1):
        curr_board = read_board_from_image(os.path.join(directory, filename))

        move = get_move(prev_board, curr_board)
        score = calculate_score(prev_board, move)

        txt_name = os.path.splitext(filename)[0] + ".txt"
        write_move_file(os.path.join(output_directory, txt_name), move, score)
        print(f"{filename}: {move} -> {score}")

        prev_board = curr_board


if __name__ == "__main__":
    run_game("test_game", "test_results")