import numpy
from pipes_v2.agent import blind_search
from pipes_v2.board import Board, PipeType, State
from pipes_v2.generate import generate_board
from pipes_v2.image_proc import download_board

if __name__ == "__main__":
    board = download_board(
        "https://www.puzzle-pipes.com/screenshots/d7facca56e0334e323d8a94456e3f0e3623c1950a327e.png",
        15,
        15,
    )
    # data = [
    #     ["1", "2a", "2a", "1"],
    #     ["2a", "3", "3", "2a"],
    #     ["2a", "3", "3", "2a"],
    #     ["1", "1", "1", "1"],
    # ]
    # board = Board(numpy.array([[PipeType(col) for col in row] for row in data]))
    # print(board.board.shape)
    state = State(board.HEIGHT, board.WIDTH)
    # state.solve(board)
    # print(state.joints.unknowns)
    state = blind_search(board)
    if state is None:
        raise
    state.print(board)
