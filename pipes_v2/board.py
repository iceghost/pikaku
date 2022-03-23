from enum import Enum, IntEnum
from typing import Optional, Tuple

import numpy
import numpy.typing


class PipeType(IntEnum):
    End = 0
    Corner = 1
    Long = 2
    Split = 3


class Joint(IntEnum):
    UNKNOWN = -1
    UNCONNECTED = 0
    CONNECTED = 1


class Joints:
    def __init__(self, height: int, width: int):
        # v for vertical, h for horizontal
        self.v_joints = numpy.full((height, width + 1), Joint.UNKNOWN, numpy.int8)
        self.h_joints = numpy.full((height + 1, width), Joint.UNKNOWN, numpy.int8)

        # initialize border for non-wrap pipe game
        self.v_joints[:, 0] = Joint.UNCONNECTED
        self.v_joints[:, -1] = Joint.UNCONNECTED
        self.h_joints[0, :] = Joint.UNCONNECTED
        self.h_joints[-1, :] = Joint.UNCONNECTED

        self.unknowns = numpy.count_nonzero(self.v_joints) + numpy.count_nonzero(
            self.h_joints
        )

    def at(self, x: int, y: int) -> Tuple[int, int, int, int]:
        top = self.h_joints[y, x]
        bottom = self.h_joints[y + 1, x]
        left = self.v_joints[y, x]
        right = self.v_joints[y, x + 1]
        return top, right, bottom, left

    def set(
        self,
        x: int,
        y: int,
        top: Optional[Joint] = None,
        right: Optional[Joint] = None,
        bottom: Optional[Joint] = None,
        left: Optional[Joint] = None,
    ):
        if top is not None:
            self.h_joints[y, x] = top
        if bottom is not None:
            self.h_joints[y + 1, x] = bottom
        if left is not None:
            self.v_joints[y, x] = left
        if right is not None:
            self.v_joints[y, x + 1] = right
