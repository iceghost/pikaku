from pipes.agent import blind_search
from pipes.board.random import random as brandom

if __name__ == "__main__":
    board = brandom(3, 3)
    print(board)
    print("\n")
    state = blind_search(board)
    if state is not None:
        print(state.apply_to(board))
    else:
        raise
    print("\n")
