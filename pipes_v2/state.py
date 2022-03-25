from copy import deepcopy

import numpy

from pipes_v2.board import Board
from pipes_v2.joint import Joint
from pipes_v2.joint.matrix import JointMatrix


def i_to_d(i: int):
    if i % 2 == 0:
        # map 0 -> ( 0, -1) (top)
        #     2 -> ( 0,  1) (bottom)
        return 0, i - 1
    else:
        #     1 -> ( 1,  0) (right)
        #     3 -> (-1,  0) (left)
        return 2 - i, 0


class State:
    def __init__(self, height: int, width: int):
        self.joints = JointMatrix(height, width)
        self.solved = numpy.full((height, width), False, dtype=numpy.bool8)

    def solve_help(self, x: int, y: int, board: Board):
        prev_config = self.joints.at(x, y)

        # filter out infeasible configurations of a pipe
        filtered = filter(
            lambda config: config.is_fit_into(prev_config),
            board.at(x, y).possible_configs(),
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
            for i, fixed_side, current_side in zip(
                range(4), fixed.sides(), prev_config.sides()
            ):
                # if this side is updated
                if fixed_side != Joint.UNKNOWN and current_side == Joint.UNKNOWN:
                    dx, dy = i_to_d(i)
                    self.solve_help(x + dx, y + dy, board)

            if self.joints.solved_at(x, y):
                self.solved[y, x] = True
        except StopIteration:
            return

    def solve(self, board: Board):
        for y in range(0, board.HEIGHT):
            for x in range(0, board.WIDTH):
                self.solve_help(x, y, board)

    def is_solved_help(self, x, y):
        if self.solved[y, x]:
            raise StopIteration
        self.solved[y, x] = True

        config = self.joints.at(x, y)

        visited = 1
        for i, _ in filter(
            lambda tup: tup[1] == Joint.CONNECTED, enumerate(config.sides())
        ):
            config[i] = Joint.UNCONNECTED
            self.joints.set(x, y, config)
            dx, dy = i_to_d(i)
            visited += self.is_solved_help(x + dx, y + dy)
        return visited

    def is_solved(self):
        if self.joints.unknowns != 0:
            return False
        # check for loops and connected components
        other = deepcopy(self)
        other.solved.fill(False)
        height, width = other.solved.shape
        try:
            visited = other.is_solved_help(0, 0)
            if visited == height * width:
                return True
            return False
        except StopIteration:
            return False

    def next_states(self, board: Board):
        for _, x, y in board.tiles():
            if self.solved[y, x]:
                continue
            prev_config = self.joints.at(x, y)
            filtered = filter(
                lambda config: config.is_fit_into(prev_config),
                board.at(x, y).possible_configs(),
            )
            for config in filtered:
                other = deepcopy(self)
                other.joints.set(x, y, config)
                other.solved[y, x] = True
                yield other
            break

    def print(self, board: Board):
        for _, x, y in board.tiles():
            print(self.joints.at(x, y), end="")
            if x == board.WIDTH - 1:
                print()
