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
