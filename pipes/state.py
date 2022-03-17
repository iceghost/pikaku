from array import array
from copy import deepcopy
from typing import List, Union

from .board.tiles import Tile
from .board import Board


class State:
    def __init__(self, height: int, width: int, state: Union[List[int], None] = None):
        self.height = height
        self.width = width
        if state is None:
            self.state = array('B', [0] * height * width)
        else:
            self.state = array('B', state)
        self.cursor = (0, 0)

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
        return sum([value * (4 ** index) for (index, value) in enumerate(self.state)])

    def at(self, x: int, y: int) -> int:
        return self.state[self.width * y + x]

    def inc_at(self, x: int, y: int) -> 'State':
        other = deepcopy(self)
        other.state[other.width * y + x] += 1
        other.cursor = (x, y)
        return other

    def next_states(self, board: Board):
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.at(x, y) == board.at(x, y).MAX_ROTATION - 1:
                    continue
                yield self.inc_at(x, y)

    def apply_to(self, board: Board) -> Board:
        tiles: List[List[Tile]] = []
        for y in range(0, board.HEIGHT):
            row: List[Tile] = []
            for x in range(0, board.WIDTH):
                step = self.at(x, y)
                tile = board.at(x, y)
                if step != 0:
                    tile = tile.rotate(step)
                row.append(tile)
            tiles.append(row)
        return Board(tiles)
