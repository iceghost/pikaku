from array import array
from copy import deepcopy
from typing import Set
from board import Board


class State:
    board: Board

    def __init__(self, size: int):
        self.size = size
        self.state = array('B', [0] * size * size)
        self.maxed: Set[int] = set()

    def at(self, x: int, y: int) -> int:
        return self.state[self.size * y + x]

    def rotate(self, pos: int) -> 'State':
        if self.state[pos] == State.board.at(pos % self.size, pos // self.size).max_rotation - 1:
            raise Exception("maximum rotation reached")
        other = deepcopy(self)
        other.state[pos] += 1
        return other

    def __iter__(self):
        pass
