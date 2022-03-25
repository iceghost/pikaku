from pipes_v2.joint.type import PipeType


class Board:
    def __init__(self, board):
        self.board = board
        self.HEIGHT, self.WIDTH = self.board.shape

    def at(self, x: int, y: int) -> PipeType:
        return PipeType(self.board[y, x])

    def tiles(self):
        for y in range(0, self.HEIGHT):
            for x in range(0, self.WIDTH):
                yield self.at(x, y), x, y
