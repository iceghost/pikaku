from random import randrange
from typing import Union
from .board.tiles import Tile
from .state import State
from .board import Board
from queue import LifoQueue


def blind_search(board: Board):
    states: LifoQueue[State] = LifoQueue()
    states.put(State(board.HEIGHT, board.WIDTH))
    while not states.empty():
        state = states.get()
        if evaluate(state, board) == 0:
            return state
        for next_state in state.next_states(board):
            states.put(next_state)
    return None


def hill_climb(board: Board, initial_state: Union[State, None] = None):
    state = State(board.HEIGHT, board.WIDTH) if initial_state is None else initial_state
    while True:
        best_score = None
        best_neighbor = None
        for neighbor in state.neighbor_states(board):
            evaluation = evaluate(neighbor, board)
            if best_score is None or evaluation < best_score:
                best_score = evaluation
                best_neighbor = neighbor
        if (
            best_neighbor is None
            or best_score is None
            or best_score >= evaluate(state, board)
        ):
            return state
        state = best_neighbor


def random_hill_climb(board: Board):
    while True:
        seed = [
            randrange(0, board.at(i % board.WIDTH, i // board.WIDTH).MAX_ROTATION)
            for i in range(0, board.HEIGHT * board.WIDTH)
        ]
        state = hill_climb(board, State(board.HEIGHT, board.WIDTH, seed))
        if evaluate(state, board) == 0:
            return state


def evaluate(state: State, board: Board):
    open_ends = 0
    new_board = state.apply_to(board)
    for y in range(0, new_board.HEIGHT):
        for x in range(0, new_board.WIDTH):
            open_ends += open_ends_at(new_board, x, y)
    return open_ends


def open_ends_at(board: Board, x: int, y: int, tile: Union[Tile, None] = None) -> int:
    if tile is None:
        tile = board.at(x, y)
    closed_end = 0
    if tile.up and y - 1 >= 0 and board.at(x, y - 1).down:
        closed_end += 1
    if tile.right and x + 1 < board.WIDTH and board.at(x + 1, y).left:
        closed_end += 1
    if tile.down and y + 1 < board.HEIGHT and board.at(x, y + 1).up:
        closed_end += 1
    if tile.left and x - 1 >= 0 and board.at(x - 1, y).right:
        closed_end += 1
    return tile.up + tile.right + tile.down + tile.left - closed_end
