from pipes_v2.agent import blind_search
from pipes_v2.board import Board
from pipes_v2.utils.image_proc import download_board
import timeit


def solve(board: Board):
    state = blind_search(board)
    if state is None:
        raise
    state.print(board)


if __name__ == "__main__":
    with open("input/15x15.txt") as file:
        for url in file.read().splitlines():
            board = download_board(url, 15, 15)
            solve(board)
            break
