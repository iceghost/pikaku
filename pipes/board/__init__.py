from typing import List
from .tiles import Tile


class Board:
    def __init__(self, board: List[List[Tile]]):
        self.board = board
        self.HEIGHT = len(board)
        self.WIDTH = len(board[0])

    def __str__(self) -> str:
        return "\n".join(["".join([str(col) for col in row]) for row in self.board])

    @staticmethod
    def from_str(raw: str):
        return Board(
            [[Tile.from_str(char) for char in line] for line in raw.splitlines()]
        )

    def at(self, x: int, y: int) -> Tile:
        return self.board[y][x]

    def tiles(self):
        for y in range(0, self.HEIGHT):
            for x in range(0, self.WIDTH):
                yield self.board[y][x]
