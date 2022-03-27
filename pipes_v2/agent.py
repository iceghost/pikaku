from dataclasses import dataclass, field
from queue import LifoQueue, PriorityQueue
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
        for state in state.next_states(x, y, board):
            states.put((state, x, y))
    return None


@dataclass(order=True)
class HeuristicItem:
    score: int
    data: Tuple[State, int, int] = field(compare=False)


def heuristic_search(board: Board):
    queue: PriorityQueue[HeuristicItem] = PriorityQueue()
    queue.put(HeuristicItem(0, (State(board.HEIGHT, board.WIDTH), 0, 0)))
    while not queue.empty():
        state, x, y = queue.get().data
        # state.solve(board)
        # print("At {}, {}".format(x, y))
        # print(state.joints)
        # print()
        try:
            state.simplify_at(x, y)
        except Solved:
            return state
        except (Looped, Detached):
            continue
        # finally:
        #     print(state.iso_joints)
        x, y = None, None
        try:
            x, y = next(
                (x, y)
                for x, y in state.next_pipes()
                if sum(1 for _ in state.next_configs(x, y, board)) == 1
            )
        except StopIteration:
            x, y = next(
                (x, y)
                for x, y in state.next_pipes()
                if sum(1 for _ in state.next_configs(x, y, board)) == 2
            )

        score = sum(1 for _ in state.next_configs(x, y, board))
        for next_state in state.next_states(x, y, board):
            queue.put(HeuristicItem(score, (next_state, x, y)))
    return None
