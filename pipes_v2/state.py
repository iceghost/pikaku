from copy import deepcopy
from typing import Dict, Set, Tuple

from pipes_v2.board import Board
from pipes_v2.joint import Joint
from pipes_v2.joint.configuration import JointConfiguration
from pipes_v2.joint.matrix import JointMatrix
from pipes_v2.utils.direction import dir_to_dx_dy


class Solved(Exception):
    pass


class Detached(Exception):
    """Violate rule: "all pipes are connected in a single group" """

    pass


class Looped(Exception):
    """Violate rule: "Closed loops are not allowed." """

    pass


class State:
    def __init__(self, height: int, width: int):
        self.HEIGHT = height
        self.WIDTH = width
        self.joints = JointMatrix(height, width)
        # keep track of underlying simplified structure
        self.iso_joints = JointMatrix(height, width)

    def solve(self, board: Board):
        """Solve pipes with only one orientation possible."""
        for y in range(0, board.HEIGHT):
            for x in range(0, board.WIDTH):
                self.solve_help(x, y, board)

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

        except StopIteration:
            return

    def simplify_at(self, x, y):
        """Check if any rule is violated or if the puzzle is solved. Raise [Looped],
        [Detached] or [Solved] respectively.
        """
        self.simplify_at_help(x, y, set(), -1)

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
            if self.iso_joints.is_closed():
                raise Solved
            else:
                raise Detached
        elif len(connecteds) == 1 and from_dir != -1:
            self.iso_joints.set_joint(x, y, from_dir, Joint.UNCONNECTED)

    def next_pipes(self, next_index=0):
        for index in range(next_index, self.HEIGHT * self.WIDTH):
            x = index % self.WIDTH
            y = index // self.WIDTH
            if self.joints.is_solved_at(x, y):
                continue
            yield x, y

    def next_configs(self, x, y, board: Board):
        prev_config = self.joints.at(x, y)
        filtered = filter(
            lambda config: config.is_fit_into(prev_config),
            board.at(x, y).possible_configs(),
        )

        def clone_and_set(config: JointConfiguration):
            other = deepcopy(self)
            other.joints.set(x, y, config)
            other.iso_joints.set(x, y, config)
            return other

        return map(clone_and_set, filtered)

    def __str__(self):
        return str(self.joints)
