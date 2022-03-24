from pipes_v2.board import Board, State
from pipes_v2.generate import generate_board
from pipes_v2.image_proc import download_board

if __name__ == "__main__":
    board = download_board(
        "https://www.puzzle-pipes.com/screenshots/6fbbfac914b0fe5d0653a4019c3c18ba623be9c08299a.png",
        25,
        25,
    )
    state = State(board.HEIGHT, board.WIDTH)
    state.solve(board)
    print(state.solved)
    for y in range(0, board.HEIGHT):
        for x in range(0, board.WIDTH):
            print(state.joints.at(x, y), end="")
        print()
