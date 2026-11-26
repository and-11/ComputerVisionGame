import os
import cv2 as cv

from config import CORNER_CELLS, COLOR_TO_CODE, COLOR_ORDER, rows, CellType, HEX_DIRECTIONS
from helpers import extrage_careu
from board_reader import extract_cells, classify_patch
from scoreboard_reader import get_scoreboard

def map_scoreboards(scoreboard_dir):
    scoreboard_map = {}

    for filename in sorted(os.listdir(scoreboard_dir)):
        if not filename.lower().endswith(".jpg"):
            continue

        img = cv.imread(os.path.join(scoreboard_dir, filename))
        if img is None:
            continue

        warped = extrage_careu(img)
        state = get_scoreboard(warped)
        scoreboard_map[tuple(state)] = filename

    return scoreboard_map


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
    score_str = " ".join(parts) if parts else "0"
    return points, score_str



def write_move_file(output_path, move, score=0):
    lines = [f"{pos} {color}" for pos, color in move]
    lines.append(str(score))
    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")





def run_game(directory, output_directory, scoreboard_map):
    os.makedirs(output_directory, exist_ok=True)

    all_images = sorted(
        f for f in os.listdir(directory) if f.lower().endswith(".jpg") and "_" in f
    )
    games = sorted(
        {f.split("_")[0] for f in all_images},
        key=lambda g: int(g) if g.isdigit() else g,
    )

    for game in games:
        game_files = [f for f in all_images if f.startswith(f"{game}_")]
        prev_board = create_initial_board()
        player_scores = [[0] * 6, [0] * 6]
        mapping_lines = []

        for step, filename in enumerate(game_files, start=1):
            curr_board = read_board_from_image(os.path.join(directory, filename))
            move = get_move(prev_board, curr_board)
            points, score_str = calculate_score(prev_board, move)

            active_player = (step - 1) % 2
            for i, code in enumerate(COLOR_ORDER):
                player_scores[active_player][i] = min(
                    18, player_scores[active_player][i] + points[code]
                )

            matched_sb = scoreboard_map.get(tuple(player_scores[active_player]))
            mapping_lines.append(f"{filename} {matched_sb}")

            txt_name = os.path.splitext(filename)[0] + ".txt"
            write_move_file(os.path.join(output_directory, txt_name), move, score_str)

            print(f"{filename}: {score_str} | {matched_sb}")
            prev_board = curr_board

        mapping_path = os.path.join(output_directory, f"{game}_mapare_table_scor.txt")
        with open(mapping_path, "w") as f:
            f.write("\n".join(mapping_lines) + "\n")



if __name__ == "__main__":
    scoreboard_map = map_scoreboards("antrenare/table-scor")
    run_game("antrenare/table-joc", "test_results", scoreboard_map)