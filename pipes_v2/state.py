from copy import deepcopy
from typing import Dict, Set, Tuple

import numpy

from pipes_v2.board import Board
from pipes_v2.joint import Joint
from pipes_v2.joint.matrix import JointMatrix
from pipes_v2.utils.direction import dir_to_dx_dy


class Solved(Exception):
    pass


class Detached(Exception):
    pass


class Looped(Exception):
    pass


class State:
    def __init__(self, height: int, width: int):
        self.HEIGHT = height
        self.WIDTH = width
        self.joints = JointMatrix(height, width)
        # keep track of underlying simplified structure
        self.iso_joints = JointMatrix(height, width)
        self.solved: Set[Tuple[int, int]] = set()

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
                for i, (fixed_joint, joint) in enumerate(
                    zip(fixed.joints(), config.joints())
                ):
                    if fixed_joint != joint:
                        fixed[i] = Joint.UNKNOWN
            self.joints.set(x, y, fixed)
            self.iso_joints.set(x, y, fixed)

            # propagate update to nearby pipes
            for i, (fixed_joint, current_joint) in enumerate(
                zip(fixed.joints(), prev_config.joints())
            ):
                # if this joint is updated
                if fixed_joint != Joint.UNKNOWN and current_joint == Joint.UNKNOWN:
                    dx, dy = dir_to_dx_dy(i)
                    self.solve_help(x + dx, y + dy, board)

            if self.joints.solved_at(x, y):
                self.solved.add((x, y))
        except StopIteration:
            return

    def solve(self, board: Board):
        for y in range(0, board.HEIGHT):
            for x in range(0, board.WIDTH):
                self.solve_help(x, y, board)

    def simplify_at_help(self, x, y, visited: Set[Tuple[int, int]], from_dir):
        if (x, y) in visited:
            raise Looped
        visited.add((x, y))

        # visit connected directions, ignore one we came from
        for dir, _ in filter(
            lambda tup: tup[0] != from_dir and tup[1].is_connected(),
            enumerate(self.iso_joints.at(x, y).joints()),
        ):
            dx, dy = dir_to_dx_dy(dir)
            self.simplify_at_help(x + dx, y + dy, visited, (dir + 2) % 4)

        joints = list(self.iso_joints.at(x, y).joints())
        connecteds = list(filter(Joint.is_connected, joints))
        # simplify graph
        if any(map(Joint.is_unknown, joints)):
            return
        if len(connecteds) == 0:
            if (
                numpy.count_nonzero(self.iso_joints.h_joints)
                + numpy.count_nonzero(self.iso_joints.v_joints)
                == 0
            ):
                raise Solved
            else:
                raise Detached
        elif len(connecteds) == 1 and from_dir != -1:
            self.iso_joints.set_joint(x, y, from_dir, Joint.UNCONNECTED)

    def simplify_at(self, x, y):
        self.simplify_at_help(x, y, set(), -1)

    def next_pipes(self, next_index=0):
        for index in range(next_index, self.HEIGHT * self.WIDTH):
            x = index % self.WIDTH
            y = index // self.WIDTH
            if (x, y) in self.solved:
                continue
            yield x, y

    def next_configs(self, x, y, board: Board):
        prev_config = self.joints.at(x, y)
        filtered = filter(
            lambda config: config.is_fit_into(prev_config),
            board.at(x, y).possible_configs(),
        )
        for config in filtered:
            other = deepcopy(self)
            other.joints.set(x, y, config)
            other.iso_joints.set(x, y, config)
            other.solved.add((x, y))
            yield other
