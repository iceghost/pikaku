from enum import Enum, IntEnum
from typing import Optional, Tuple


class PipeType(Enum):
    End = 0
    Corner = 1
    Long = 2
    Split = 3


class Joint(IntEnum):
    Unknown = 0
    Connected = 1
    Unconnected = 2


class Joints:
    def __init__(self, height: int, width: int):
        # v for vertical, h for horizontal
        self.v_joints = [[Joint.Unknown] * (width + 1) for _ in range(0, height)]
        self.h_joints = [[Joint.Unknown] * (width) for _ in range(0, height + 1)]

    def at(self, x: int, y: int) -> Tuple[Joint, Joint, Joint, Joint]:
        top = self.h_joints[y][x]
        bottom = self.h_joints[y + 1][x]
        left = self.v_joints[y][x]
        right = self.v_joints[y][x + 1]
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
            self.h_joints[y][x] = top
        if bottom is not None:
            self.h_joints[y + 1][x] = bottom
        if left is not None:
            self.v_joints[y][x] = left
        if right is not None:
            self.v_joints[y][x + 1] = right
