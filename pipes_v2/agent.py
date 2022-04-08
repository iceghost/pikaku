import logging
from queue import LifoQueue
from typing import Tuple
from pipes_v2.board import Board
from pipes_v2.state import Detached, Looped, Solved, State


def blind_search(board: Board):
    states: LifoQueue[Tuple[State, int, int]] = LifoQueue()
    explored = 0
    states.put((State(board.HEIGHT, board.WIDTH), 0, 0))
    while not states.empty():
        state, x, y = states.get()
        explored += 1
        # if state in visited:
        #     raise
        # visited.add(state)

        # logging.debug("joints: \n{}".format(state.joints))
        try:
            state.simplify_at(x, y)
            # logging.debug("iso-joints: \n{}".format(state.iso_joints))
        except Solved:
            logging.info("explored: {}".format(explored))
            return state
        except (Looped, Detached):
            continue

        next_x, next_y = next(state.next_pipes())
        for next_state in state.next_states(next_x, next_y, board):
            states.put((next_state, next_x, next_y))


def heuristic_search(board: Board):
    queue: LifoQueue[Tuple[State, int, int]] = LifoQueue()
    queue.put((State(board.HEIGHT, board.WIDTH), 0, 0))
    explored = 0
    while not queue.empty():
        state, x, y = queue.get()
        explored += 1

        try:
            state.simplify_at(x, y)
        except Solved:
            logging.info("explored: {}".format(explored))
            return state
        except (Looped, Detached):
            continue

        x, y = min(
            state.next_pipes(),
            key=lambda tup: len(list(state.next_configs(tup[0], tup[1], board))),
        )
        for next_state in state.next_states(x, y, board):
            queue.put((next_state, x, y))


def improved_search(board: Board):
    queue: LifoQueue[Tuple[State, int, int]] = LifoQueue()
    queue.put((State(board.HEIGHT, board.WIDTH), 0, 0))
    explored = 0
    while not queue.empty():
        state, x, y = queue.get()
        explored += 1
        state.solve(board)

        try:
            state.simplify_at(x, y)
        except Solved:
            logging.info("explored: {}".format(explored))
            return state
        except (Looped, Detached):
            continue

        next_x, next_y = next(state.next_pipes())
        for next_state in state.next_states(next_x, next_y, board):
            queue.put((next_state, next_x, next_y))


def demo_search(board: Board):
    queue: LifoQueue[Tuple[State, int, int]] = LifoQueue()
    queue.put((State(board.HEIGHT, board.WIDTH), 0, 0))
    while not queue.empty():
        state, x, y = queue.get()
        yield state, (x, y, "Try a configuration at ({: >2}, {: >2})".format(x, y))
        # state.solve(board)
        # yield state, (None, None, "Solve easy pipes")
        try:
            state.simplify_at(x, y)
        except Solved:
            yield state, (None, None, "Solved")
            return
        except Looped:
            yield state, (x, y, "Looped near ({: >2}, {: >2})".format(x, y))
            continue
        except Detached:
            yield state, (x, y, "Detached near ({: >2}, {: >2})".format(x, y))
            continue

        next_x, next_y = next(state.next_pipes())
        for next_state in state.next_states(next_x, next_y, board):
            queue.put((next_state, next_x, next_y))
