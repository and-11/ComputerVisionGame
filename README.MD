
# How to Run

---

1. Update the dataset and output paths in `config.py`:

```
   PATH_RESULT = "test_results"

   PATH_SCORE_BOARD = "antrenare/table-scor"

   PATH_GAMES = "antrenare/table-joc"
```


2. Run the main script:

```
   python3 main.py
```











## Libraries Used

- External: cv2, numpy
- Standard Library: os, enum





## Project Structure & Functions


config.py

- Stores input/output folder paths, board and scoreboard grid calibration constants (centers, pitch, offsets), HSV hue ranges, visualization colors, and the CellType enum.



main.py

- Entry point that builds the scoreboard lookup dictionary and runs the full game tracking pipeline.



helpers.py

- show_image: Resizes an image and displays it in a window until a key is pressed.

- extrage_careu: Detects the board and applies a perspective warp to flatten it.

- draw_cells: Draws the cell boundaries for visual debugging.

- get_cell_center: Computes the (x, y) pixel coordinates of a hexagonal cell from its (row, col) indices.



board_reader.py

- extract_cells: Crops square image patches centered on every hexagonal cell of the warped board.

- classify_patch: Identifies whether a cell patch is empty or holds a specific colored tile using HSV thresholds and hue histograms.

- visualize_patches: Draws color-coded rectangles over classified board cells to verify detection accuracy.

- get_considered_pixels: Masks and displays only the bright, saturated symbol pixels used during tile classification.



scoreboard_reader.py

- draw_grid: Draws the 19x6 scoreboard grid overlay onto an image.

- set_grid: Opens an interactive OpenCV trackbar window to tune the scoreboard grid coordinates and cell dimensions.

- classify_score_patch: Classifies a single scoreboard cell patch using median HSV values.
(-> no longer used when i relyed on it it gave me multiple scores for one color)


- get_scoreboard: Finds the cube score (0-18) in each of the 6 color columns by selecting the row with the most matching colored pixels.



game_logic.py

- map_scoreboards: Maps 6-color score tuples from reference scoreboard images to their filenames.

- _build_position_maps: Builds lookup dictionaries converting between (row, col) grid indices and 1-based board positions.

- rc_to_pos: Converts (row, col) indices into a board position number.

- pos_to_rc: Converts a board position number back into (row, col) indices.

- rc_to_axial: Converts offset (row, col) board coordinates to axial (q, r) hex coordinates.

- axial_to_rc: Converts axial (q, r) hex coordinates back to offset (row, col) board coordinates.

- create_initial_board: Creates an empty board populated with the 6 fixed starting corner pieces.

- print_board: Prints a text representation of the board state to the console.

- read_board_from_image: Reads a game image, warps it, and returns the classified 2D board grid.

- get_move: Compares two consecutive board states to detect newly placed tiles and their positions.

- calculate_score: Computes points earned across all 6 hex directions for a move and formats the score string.

- write_move_file: Writes a move's tile placements and earned score to a .txt output file.

- run_game: Processes all game sequences in a directory, tracks player scores, and saves move and scoreboard mapping .txt files.