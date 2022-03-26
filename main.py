import logging
from pipes_v2.agent import blind_search
from pipes_v2.board import Board
from pipes_v2.utils.generate import generate_board
from pipes_v2.utils.image_proc import download_board
import timeit


logging.basicConfig(level=logging.INFO)


def solve(board: Board):
    state = blind_search(board)
    if state is None:
        raise
    print(state.joints)


if __name__ == "__main__":
    board = download_board(
        "https://www.puzzle-pipes.com/screenshots/99b4ed7ba120036f5b5afac51206910b623e78d639129.png",
        60,
        40,
    )
    # board = generate_board(40, 60)
    print(timeit.timeit("solve(board)", number=1, globals=locals()))
