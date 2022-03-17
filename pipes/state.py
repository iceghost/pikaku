from array import array
from copy import deepcopy
from typing import List, Union
from .board import Board


class State:
    def __init__(self, height: int, width: int, state: Union[List[int], None] = None):
        self.height = height
        self.width = width
        if state is None:
            self.state = array("B", [0] * height * width)
        else:
            assert len(state) == height * width
            self.state = array("B", state)
        self.cursor = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            raise NotImplemented
        if self.height != other.height or self.width != other.width:
            return False
        for i in range(0, self.height * self.width):
            if self.state[i] != other.state[i]:
                return False
        return True

    def __hash__(self) -> int:
        return sum([value * (4**index) for (index, value) in enumerate(self.state)])

    def at(self, x: int, y: int) -> int:
        return self.state[self.width * y + x]

    def next_states(self, board: Board):
        for cursor in range(self.cursor, self.height * self.width):
            x = cursor % self.width
            y = cursor // self.width
            if self.state[cursor] == board.at(x, y).MAX_ROTATION - 1:
                continue
            other = deepcopy(self)
            other.state[cursor] += 1
            other.cursor = cursor
            yield other

    def apply_to(self, board: Board) -> Board:
        tiles = [
            tile.rotate(self.state[i]) if self.state[i] != 0 else tile
            for (i, tile) in enumerate(board.tiles())
        ]
        return Board(
            [tiles[i : i + board.WIDTH] for i in range(0, len(tiles), board.WIDTH)]
        )
