from typing import Optional, Set, Tuple
from random import Random, randrange, shuffle

import sys
import numpy
import logging

from pipes_v2.joint import Joint
from pipes_v2.joint.configuration import JointConfiguration
from pipes_v2.joint.type import PipeType
from pipes_v2.state import State
from pipes_v2.board import Board
from pipes_v2.utils.direction import dir_to_dx_dy


def generate_board(height: int, width: int, seed: Optional[int] = None) -> "Board":
    seed = seed if seed is not None else randrange(sys.maxsize)
    random = Random(seed)
    sys.setrecursionlimit(max(1000, height * width))
    while True:
        try:
            state = State(height, width)
            visit(state, 0, 0, set(), random)
            board = Board(
                numpy.array(
                    [
                        [get_tile_type(state.joints.at(x, y)) for x in range(0, width)]
                        for y in range(0, height)
                    ],  # type:ignore
                )
            )
            logging.info("Generated board of seed %i", seed)
            logging.debug("Goal: \n" + str(state.joints))
            logging.debug("Board: \n" + str(board))
            return board
        except InvalidTile:
            continue


def visit(
    state: State,
    x: int,
    y: int,
    visited: Set[Tuple[int, int]],
    random: Random,
    from_dir=-1,
) -> bool:
    if x < 0 or y < 0 or x >= state.WIDTH or y >= state.HEIGHT or (x, y) in visited:
        return False
    visited.add((x, y))
    if from_dir != -1:
        state.joints.set_joint(x, y, from_dir, Joint.CONNECTED)

    dirs = list(enumerate(state.joints.at(x, y).joints()))
    random.shuffle(dirs)
    dirs = filter(lambda tup: tup[1].is_unknown(), dirs)
    for dir, _ in dirs:
        dx, dy = dir_to_dx_dy(dir)
        if not visit(state, x + dx, y + dy, visited, random, (dir + 2) % 4):
            state.joints.set_joint(x, y, dir, Joint.UNCONNECTED)

    return True


class InvalidTile(Exception):
    pass


def get_tile_type(config: JointConfiguration):
    if any(joint == Joint.UNKNOWN for joint in config.joints()):
        raise InvalidTile
    joints = config.top + config.bottom + config.left + config.right
    if joints == 1:
        return PipeType.End
    if joints == 2:
        if (config.top and config.bottom) or (config.left and config.right):
            return PipeType.Long
        else:
            return PipeType.Corner
    if joints == 3:
        return PipeType.Split
    raise InvalidTile
