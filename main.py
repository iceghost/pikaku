import logging
from pipes_v2.agent import blind_search, heuristic_search
from pipes_v2.board import Board
from pipes_v2.utils.iterator import exhaust
from pipes_v2.utils.generate import generate_board
from pipes_v2.utils.image_proc import download_board
import timeit


logging.basicConfig(level=logging.INFO)


def blind_solve(board: Board):
    state, _ = exhaust(blind_search(board))
    if state is None:
        raise
    print(state.joints)


def heuristic_solve(board: Board):
    state = exhaust(heuristic_search(board))
    if state is None:
        raise
    print(state.joints)


if __name__ == "__main__":
    board = download_board(
        "https://www.puzzle-pipes.com/screenshots/69becb4d45af49d9a092e1a9d1e5ce0b62411aa22a250.png",
        40,
        40,
    )
    print(timeit.timeit("blind_solve(board)", number=1, globals=locals()))
    print(timeit.timeit("heuristic_solve(board)", number=1, globals=locals()))
