from pipes_v2.agent import blind_search
from pipes_v2.board import Board, PipeType, State
from pipes_v2.generate import generate_board
from pipes_v2.image_proc import download_board
import timeit


def solve(board: Board):
    state = blind_search(board)
    if state is None:
        raise


if __name__ == "__main__":
    with open("input/15x15.txt") as file:
        for url in file.read().splitlines():
            board = download_board(url, 15, 15)
            print(timeit.repeat("solve(board)", repeat=5, number=1, globals=locals()))
