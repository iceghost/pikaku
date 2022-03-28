from dataclasses import dataclass, field
from enum import Enum
from queue import LifoQueue, PriorityQueue
from typing import Optional, Tuple
from pipes_v2.board import Board
from pipes_v2.state import Detached, Looped, Solved, State


class Status(Enum):
    TRY = 0
    SOLVE = 1
    SOLVED = 2
    LOOPED = 3
    DETACHED = 4
    DEADEND = 5

    def message(self, x, y):
        if self is Status.TRY:
            return "Thử hướng quay tại ({: >2}, {: >2})".format(x, y)
        elif self is Status.SOLVE:
            return "Giải các ô chỉ có một hướng xoay"
        elif self is Status.SOLVED:
            return "Bàn cờ đã được giải"
        elif self is Status.LOOPED:
            return (
                "Phát hiện vi phạm luật vòng lặp khi duyệt tại ({: >2}, {: >2})".format(
                    x, y
                )
            )
        elif self is Status.DETACHED:
            return (
                "Phát hiện vi phạm luật kết nối khi duyệt tại ({: >2}, {: >2})".format(
                    x, y
                )
            )
        elif self is Status.DEADEND:
            return "Ô ({: >2}, {: >2}) không thể xoay đi đâu nữa".format(x, y)
        else:
            return "... what"


def blind_search(board: Board):
    states: LifoQueue[Tuple[State, int, int]] = LifoQueue()
    states.put((State(board.HEIGHT, board.WIDTH), 0, 0))
    while not states.empty():
        state, x, y = states.get()
        yield state, (x, y, Status.TRY)
        # state.solve(board)
        # yield state, (x, y, Status.SOLVE)
        try:
            state.simplify_at(x, y)
        except Solved:
            yield state, (None, None, Status.SOLVED)
            return
        except Looped:
            yield state, (x, y, Status.LOOPED)
            continue
        except Detached:
            yield state, (x, y, Status.DETACHED)
            continue

        x, y = next(state.next_pipes())
        if sum(1 for _ in state.next_configs(x, y, board)) == 0:
            yield state, (x, y, Status.DEADEND)
        else:
            for state in state.next_states(x, y, board):
                states.put((state, x, y))
    return


@dataclass(order=True)
class HeuristicItem:
    score: int
    data: Tuple[State, int, int] = field(compare=False)


def heuristic_search(board: Board):
    queue: PriorityQueue[HeuristicItem] = PriorityQueue()
    queue.put(HeuristicItem(0, (State(board.HEIGHT, board.WIDTH), 0, 0)))
    while not queue.empty():
        state, x, y = queue.get().data
        yield state
        state.solve(board)
        yield state
        try:
            state.simplify_at(x, y)
        except Solved:
            return
        except (Looped, Detached):
            continue
        # finally:
        #     print(state.iso_joints)
        x, y, score = None, None, 2
        while True:
            try:
                x, y = next(
                    (x, y)
                    for x, y in state.next_pipes()
                    if sum(1 for _ in state.next_configs(x, y, board)) == score
                )
                break
            except StopIteration:
                score = score + 1

        for next_state in state.next_states(x, y, board):
            queue.put(HeuristicItem(score, (next_state, x, y)))
