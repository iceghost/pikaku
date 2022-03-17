from pipes.agent import blind_search, evaluate, hill_climb, random_hill_climb
from pipes.board.random import random as brandom
from pipes.state import State

if __name__ == "__main__":
    board = brandom(10, 10)
    print(board)
    print(evaluate(State(board.WIDTH, board.HEIGHT), board))
    print("\n")
    state = random_hill_climb(board)
    if state is not None:
        new_board = state.apply_to(board)
        print(new_board)
        print(evaluate(State(new_board.WIDTH, new_board.HEIGHT), new_board))
    else:
        raise
    print("\n")
