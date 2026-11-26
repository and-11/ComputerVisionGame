from game_logic import map_scoreboards, run_game



if __name__ == "__main__":
    scoreboard_map = map_scoreboards("antrenare/table-scor")
    run_game("antrenare/table-scor", "test_results", scoreboard_map)

    