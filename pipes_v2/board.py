import numpy
import numpy.typing
from pipes_v2.joint.type import PipeType


class Board:
    def __init__(self, board: numpy.typing.NDArray):
        self.board = board
        self.HEIGHT, self.WIDTH = self.board.shape

    def at(self, x: int, y: int) -> PipeType:
        return PipeType(self.board[y, x])

    def __str__(self):
        return "\n".join(
            " ".join(self.at(x, y).value.ljust(2) for x in range(0, self.WIDTH))
            for y in range(0, self.HEIGHT)
        )
