from game_logic import map_scoreboards, run_game
import config  


if __name__ == "__main__":



    scoreboard_map = map_scoreboards(config.PATH_SCORE_BOARD)
    run_game(config.PATH_GAMES, config.PATH_RESULT, scoreboard_map)

    