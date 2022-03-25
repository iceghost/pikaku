from copy import deepcopy

import numpy

from pipes_v2.board import Board
from pipes_v2.joint import Joint
from pipes_v2.joint.matrix import JointMatrix
from pipes_v2.utils.direction import dir_to_dx_dy


class State:
    def __init__(self, height: int, width: int):
        self.joints = JointMatrix(height, width)
        self.solved = numpy.full((height, width), False, dtype=numpy.bool8)

    def solve_help(self, x: int, y: int, board: Board):
        prev_config = self.joints.at(x, y)

        # filter out infeasible configurations of a pipe
        filtered = filter(
            prev_config.is_fit_into,
            board.at(x, y).possible_configs(),
        )

        # check if exist "fixed" joint
        try:
            fixed = next(filtered)
            for config in filtered:
                for (i, (fixed_joint, joint)) in enumerate(
                    zip(fixed.joints(), config.joints())
                ):
                    if fixed_joint != joint:
                        fixed[i] = Joint.UNKNOWN
            self.joints.set(x, y, fixed)

            # propagate update to nearby pipes
            for i, fixed_joint, current_joint in zip(
                range(4), fixed.joints(), prev_config.joints()
            ):
                # if this joint is updated
                if fixed_joint != Joint.UNKNOWN and current_joint == Joint.UNKNOWN:
                    dx, dy = dir_to_dx_dy(i)
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
        for dir, _ in filter(
            lambda tup: tup[1].is_connected(), enumerate(config.joints())
        ):
            self.joints.set_joint(x, y, dir, Joint.UNCONNECTED)
            dx, dy = dir_to_dx_dy(dir)
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
