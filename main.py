from pipes_v2.agent import blind_search
from pipes_v2.board import Board
from pipes_v2.utils.image_proc import download_board
import timeit


def solve(board: Board):
    state = blind_search(board)
    if state is None:
        raise
    print(state.joints)


if __name__ == "__main__":
    # with open("input/15x15.txt") as file:
    #     for url in file.read().splitlines():
    #         board = download_board(url, 15, 15)
    #         solve(board)
    #         break
    board = download_board(
        "https://www.puzzle-pipes.com/screenshots/d1f6571368154581b6a7d4b2e91d1bcd623dd64a1b281.png",
        15,
        15,
    )
    print(timeit.timeit("solve(board)", number=1, globals=locals()))
