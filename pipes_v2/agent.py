from queue import LifoQueue
from pipes_v2.board import Board
from pipes_v2.state import State


def blind_search(board: Board):
    states: LifoQueue[State] = LifoQueue()
    states.put(State(board.HEIGHT, board.WIDTH))
    while not states.empty():
        state = states.get()
        state.solve(board)
        # state.print(board)
        if state.is_solved():
            return state
        for next_state in state.next_states(board):
            states.put(next_state)
    return None