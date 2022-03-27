import logging
from pipes_v2.agent import blind_search, heuristic_search
from pipes_v2.board import Board
from pipes_v2.utils.generate import generate_board
from pipes_v2.utils.image_proc import download_board
import timeit


logging.basicConfig(level=logging.INFO)


def blind_solve(board: Board):
    state = blind_search(board)
    if state is None:
        raise
    print(state.joints)


def heuristic_solve(board: Board):
    state = heuristic_search(board)
    if state is None:
        raise
    print(state.joints)


if __name__ == "__main__":
    # board = download_board(
    #     "https://www.puzzle-pipes.com/screenshots/62d5c0adc7cdca26790fce8ea96cdee5623c4d9b521e6.png",
    #     15,
    #     15,
    # )
    board = generate_board(30, 30)
    print(timeit.timeit("blind_solve(board)", number=1, globals=locals()))
    print(timeit.timeit("heuristic_solve(board)", number=1, globals=locals()))
