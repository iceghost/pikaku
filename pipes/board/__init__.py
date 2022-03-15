from typing import List
from .tiles import Tile

class Board:
    def __init__(self, board: List[List[Tile]]):
        self.board = board
        self.size = len(board)

    def __str__(self) -> str:
        return "\n".join(["".join([str(col) for col in row]) for row in self.board])

    def at(self, x: int, y: int) -> Tile:
        return self.board[y][x]

    def rotate(self, x: int, y: int):
        self.board[y][x] = self.board[y][x].rotate()

    def __len__(self) -> int:
        return self.size

    def is_solved(self) -> bool:
        visited = [[False] * self.size for _ in range(0, self.size)]
        return self._reachable_from_help(0, 0, visited) == self.size ** 2

    def _reachable_from_help(self, x: int, y: int, visited: List[List[bool]]) -> int:
        if x < 0 or x >= self.size or y < 0 or y >= self.size:
            return 0
        if visited[y][x]:
            return 0
        visited[y][x] = True
        reachable = 1  # self count
        if self.board[y][x].up and y - 1 >= 0 and self.board[y - 1][x].down:
            reachable += self._reachable_from_help(x, y - 1, visited)
        if self.board[y][x].right and x + 1 < self.size and self.board[y][x + 1].left:
            reachable += self._reachable_from_help(x + 1, y, visited)
        if self.board[y][x].down and y + 1 < self.size and self.board[y + 1][x].up:
            reachable += self._reachable_from_help(x, y + 1, visited)
        if self.board[y][x].left and x - 1 >= 0 and self.board[y][x - 1].right:
            reachable += self._reachable_from_help(x - 1, y, visited)
        return reachable
