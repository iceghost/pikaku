from enum import Enum, IntEnum
from typing import Optional, Tuple

import numpy
import numpy.typing


class PipeType(IntEnum):
    End = 0
    Corner = 1
    Long = 2
    Split = 3


def possible_configs(type: PipeType):
    # initial rotation
    initial = JointConfiguration(
        top=Joint.CONNECTED,
        right=Joint.UNCONNECTED,
        bottom=Joint.UNCONNECTED,
        left=Joint.UNCONNECTED,
    )
    if type == PipeType.Corner or type == PipeType.Split:
        initial.right = Joint.CONNECTED
    if type == PipeType.Long or type == PipeType.Split:
        initial.bottom = Joint.CONNECTED

    max_rotation = 2 if type == PipeType.Long else 4
    for _ in range(0, max_rotation):
        yield initial
        initial.rotate_right()


class Joint(IntEnum):
    UNKNOWN = -1
    UNCONNECTED = 0
    CONNECTED = 1


class JointConfiguration:
    def __init__(
        self,
        top: Joint = Joint.UNKNOWN,
        right: Joint = Joint.UNKNOWN,
        bottom: Joint = Joint.UNKNOWN,
        left: Joint = Joint.UNKNOWN,
    ) -> None:
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        pass

    def rotate_right(self):
        self.top, self.right, self.bottom, self.left = (
            self.left,
            self.top,
            self.right,
            self.bottom,
        )

    def is_fit_into(self, config: "JointConfiguration"):
        def fit_joint(this: Joint, that: Joint):
            return this == that or this == Joint.UNKNOWN or that == Joint.UNKNOWN

        return (
            fit_joint(self.top, config.top)
            and fit_joint(self.right, config.right)
            and fit_joint(self.bottom, config.bottom)
            and fit_joint(self.left, config.left)
        )

    def sides(self):
        yield self.top
        yield self.right
        yield self.bottom
        yield self.left

    def __getitem__(self, key):
        if key == 0:
            return self.top
        if key == 1:
            return self.right
        if key == 2:
            return self.bottom
        if key == 3:
            return self.left

    def __setitem__(self, key, value):
        if key == 0:
            self.top = value
        if key == 1:
            self.right = value
        if key == 2:
            self.bottom = value
        if key == 3:
            self.left = value


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

    def at(self, x: int, y: int):
        top = self.h_joints[y, x]
        bottom = self.h_joints[y + 1, x]
        left = self.v_joints[y, x]
        right = self.v_joints[y, x + 1]
        return JointConfiguration(Joint(top), Joint(right), Joint(bottom), Joint(left))

    def solved_at(self, x: int, y: int):
        config = self.at(x, y)
        return (
            config.top != Joint.UNKNOWN
            and config.bottom != Joint.UNKNOWN
            and config.left != Joint.UNKNOWN
            and config.right != Joint.UNKNOWN
        )

    def set(self, x: int, y: int, config: JointConfiguration):
        if config.top != Joint.UNKNOWN:
            self.h_joints[y, x] = config.top
            self.unknowns -= 1
        if config.bottom != Joint.UNKNOWN:
            self.h_joints[y + 1, x] = config.bottom
            self.unknowns -= 1
        if config.left != Joint.UNKNOWN:
            self.v_joints[y, x] = config.left
            self.unknowns -= 1
        if config.right != Joint.UNKNOWN:
            self.v_joints[y, x + 1] = config.right
            self.unknowns -= 1


class Board:
    def __init__(self, height: int, width: int) -> None:
        self.HEIGHT = height
        self.WIDTH = width
        self.board = numpy.ndarray((height, width), dtype=numpy.uint8)

    def at(self, x: int, y: int):
        return PipeType(self.board[y, x])


class State:
    def __init__(self, height: int, width: int):
        self.joints = Joints(height, width)
        self.solved = numpy.zeros((height, width), dtype=numpy.bool8)

    def solve_help(self, x: int, y: int, board: Board):
        prev_config = self.joints.at(x, y)

        # filter out infeasible configurations of a pipe
        filtered = filter(
            lambda config: config.is_fit_into(prev_config),
            possible_configs(board.at(x, y)),
        )

        # check if exist "fixed" side
        try:
            fixed = filtered.__next__()
            for config in filtered:
                for (i, fixed_side, side) in zip(
                    range(4), fixed.sides(), config.sides()
                ):
                    if fixed_side != side:
                        fixed[i] = Joint.UNKNOWN
            self.joints.set(x, y, fixed)

            # propagate update to nearby pipes
            something_changed = False
            for i, fixed_side, current_side in zip(
                range(4), fixed.sides(), prev_config.sides()
            ):
                # if this side is updated
                if fixed_side != Joint.UNKNOWN and current_side == Joint.UNKNOWN:
                    if i % 2 == 0:
                        # map 0 -> ( 0, -1) (top)
                        #     2 -> ( 0,  1) (bottom)
                        self.solve_help(x, y + i - 1, board)
                    else:
                        #     1 -> ( 1,  0) (right)
                        #     3 -> (-1,  0) (left)
                        self.solve_help(x + 2 - i, y, board)
                    something_changed = True

            return something_changed
        except StopIteration:
            return

    def solve(self, board: Board):
        for y in range(0, board.HEIGHT):
            for x in range(0, board.WIDTH):
                self.solve_help(x, y, board)
