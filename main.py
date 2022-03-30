import logging
from pipes_v2.agent import blind_search, heuristic_search, fast_search
from pipes_v2.board import Board
from pipes_v2.utils.iterator import exhaust
from pipes_v2.utils.generate import generate_board
from pipes_v2.utils.image_proc import download_board
import timeit


logging.basicConfig(level=logging.DEBUG)


def solve(board: Board, search_algorithm):
    state = search_algorithm(board)
    if state is None:
        raise
    logging.info("Result:\n{}".format(state.joints))


if __name__ == "__main__":
    board = download_board(
        "https://www.puzzle-pipes.com/screenshots/4154dfb2feb62e923c64ce28ae86d2236243dae951f47.png",
        20,
        20,
    )
    # print(timeit.timeit("solve(board, heuristic_search)", number=1, globals=locals()))
    print(timeit.timeit("solve(board, blind_search)", number=1, globals=locals()))
    # print(timeit.timeit("solve(board, fast_search)", number=1, globals=locals()))
