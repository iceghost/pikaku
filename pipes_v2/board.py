import numpy
import numpy.typing
from enum import Enum

from pipes_v2.joint import Joint
from pipes_v2.joint.configuration import JointConfiguration


class PipeType(Enum):
    End = "1"
    Corner = "2a"
    Long = "2b"
    Split = "3"

    def max_rotation(self):
        if self == PipeType.Long:
            return 2
        else:
            return 4

    def possible_configs(self):
        # initial rotation
        initial = JointConfiguration(
            top=Joint.CONNECTED,
            right=Joint.UNCONNECTED,
            bottom=Joint.UNCONNECTED,
            left=Joint.UNCONNECTED,
        )
        if self == PipeType.Corner or self == PipeType.Split:
            initial.right = Joint.CONNECTED
        if self == PipeType.Long or self == PipeType.Split:
            initial.bottom = Joint.CONNECTED

        for _ in range(0, self.max_rotation()):
            yield initial
            initial = initial.rotate_right()


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
