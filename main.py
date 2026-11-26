from game_logic import map_scoreboards, run_game



if __name__ == "__main__":
    scoreboard_map = map_scoreboards("task/antrenare/table-scor")
    run_game("test_game", "test_results", scoreboard_map)

    