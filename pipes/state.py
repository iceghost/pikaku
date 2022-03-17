from array import array
from copy import deepcopy
from typing import Iterator, List, Union
from .board import Board


class State:
    def __init__(self, height: int, width: int, state: Union[List[int], None] = None):
        self.HEIGHT = height
        self.WIDTH = width
        if state is None:
            self.state = array("B", [0] * height * width)
        else:
            assert len(state) == height * width
            self.state = array("B", state)
        self.cursor = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            raise NotImplemented
        if self.HEIGHT != other.HEIGHT or self.WIDTH != other.WIDTH:
            return False
        for i in range(0, self.HEIGHT * self.WIDTH):
            if self.state[i] != other.state[i]:
                return False
        return True

    def __hash__(self) -> int:
        """Hash the state using base 4 encoding"""
        return sum([value * (4**index) for (index, value) in enumerate(self.state)])

    def at(self, x: int, y: int) -> int:
        return self.state[self.WIDTH * y + x]

    def next_states(self, board: Board) -> Iterator["State"]:
        """Generate next states by increasing each rotation from cursor by 1.

        Example:

        - [0, 0, 0], cursor = 0 will generate [1, 0, 0], [0, 1, 0], [0, 0, 1]
        - [0, 0, 0], cursor = 1 will generate [0, 1, 0], [0, 0, 1]

        If the state is invalid (rotation >= MAX_ROTATION), it won't be generated
        """
        for cursor in range(self.cursor, self.HEIGHT * self.WIDTH):
            x = cursor % self.WIDTH
            y = cursor // self.WIDTH
            if self.state[cursor] == board.at(x, y).MAX_ROTATION - 1:
                continue
            other = deepcopy(self)
            other.state[cursor] += 1
            other.cursor = cursor
            yield other

    def neighbor_states(self, board: Board) -> Iterator["State"]:
        for cursor in range(0, self.HEIGHT * self.WIDTH):
            x = cursor % self.WIDTH
            y = cursor // self.WIDTH
            if self.state[cursor] > 0:
                other = deepcopy(self)
                other.state[cursor] -= 1
                yield other
            if self.state[cursor] < board.at(x, y).MAX_ROTATION - 1:
                other = deepcopy(self)
                other.state[cursor] += 1
                yield other

    def apply_to(self, board: Board) -> Board:
        """Apply state to board, generate new board, without modify old board."""
        tiles = [
            tile.rotate(self.state[i]) if self.state[i] != 0 else tile
            for (i, tile) in enumerate(board.tiles())
        ]
        return Board(
            [tiles[i : i + board.WIDTH] for i in range(0, len(tiles), board.WIDTH)]
        )
