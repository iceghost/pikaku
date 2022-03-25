from pipes_v2.joint import Joint
from pipes_v2.joint.configuration import JointConfiguration
from pipes_v2.joint.type import PipeType
from pipes_v2.state import State
from pipes_v2.board import Board
from random import shuffle


def visit(state: State, x: int, y: int) -> bool:
    try:
        if x < 0 or y < 0 or state.solved[y, x]:
            return False
    except IndexError:
        return False

    state.solved[y, x] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    shuffle(dirs)
    for (dx, dy) in dirs:
        if visit(state, x + dx, y + dy):
            if dx == -1 and dy == 0:
                state.joints.set(x, y, JointConfiguration(left=Joint.CONNECTED))
            elif dx == 1 and dy == 0:
                state.joints.set(x, y, JointConfiguration(right=Joint.CONNECTED))
            elif dx == 0 and dy == -1:
                state.joints.set(x, y, JointConfiguration(top=Joint.CONNECTED))
            else:
                state.joints.set(x, y, JointConfiguration(bottom=Joint.CONNECTED))
    return True


def generate_board(height: int, width: int) -> "Board":
    state = State(height, width)
    state.joints.h_joints.fill(Joint.UNCONNECTED)
    state.joints.v_joints.fill(Joint.UNCONNECTED)
    visit(state, 0, 0)
    print("Generated:")
    for y in range(0, height):
        for x in range(0, width):
            print(state.joints.at(x, y), end="")
        print()
    board = Board(
        [
            [get_tile_type(state.joints.at(x, y)) for x in range(0, width)]
            for y in range(0, height)
        ]  # type:ignore
    )
    return board


def get_tile_type(config: JointConfiguration):
    if any(joint == Joint.UNKNOWN for joint in config.joints()):
        return None
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
    raise
