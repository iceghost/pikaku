from queue import LifoQueue
from typing import Tuple
from pipes_v2.board import Board
from pipes_v2.state import Detached, Looped, Solved, State


def blind_search(board: Board):
    states: LifoQueue[Tuple[State, int, int]] = LifoQueue()
    states.put((State(board.HEIGHT, board.WIDTH), 0, 0))
    while not states.empty():
        state, x, y = states.get()
        # state.solve(board)
        # print("At {}, {}".format(x, y))
        # state.joints.print(board)
        # print()
        try:
            state.simplify_at(x, y)
            # state.iso_joints.print(board)
        except Solved:
            return state
        except (Looped, Detached):
            continue

        x, y = next(state.next_pipes())
        for state in state.next_configs(x, y, board):
            states.put((state, x, y))
    return None
