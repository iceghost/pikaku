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
    # print(state.joints)


if __name__ == "__main__":
    # board = download_board(
    #     "https://www.puzzle-pipes.com/screenshots/d1f6571368154581b6a7d4b2e91d1bcd623dd64a1b281.png",
    #     15,
    #     15,
    # )
    board = generate_board(25, 25)
    print(timeit.timeit("solve(board)", number=1, globals=locals()))
