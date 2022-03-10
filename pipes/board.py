import random
from typing import List
from tile import ProtoTile, Tile


class Board:
    def __init__(self, board: List[List[Tile]]):
        self.board = board
        self.size = len(board)

    @staticmethod
    def random(size: int) -> 'Board':
        protoboard = [[ProtoTile() for _ in range(0, size)] for _ in range(0, size)]
        visit(protoboard, 0, 0)
        board = Board([[Tile.from_prototile(col) for col in row] for row in protoboard])
        for x in range(0, len(board)):
            for y in range(0, len(board)):
                tile = board.at(x, y)
                for _ in range(0, random.randrange(0, tile.MAX_ROTATION - 1)):
                    board.rotate(x, y)
        return board

    def __str__(self) -> str:
        return "\n".join(["".join([col.to_char() for col in row]) for row in self.board])

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
        reachable = 1 # self count
        if self.board[y][x].up() and y - 1 >= 0 and self.board[y - 1][x].down():
            reachable += self._reachable_from_help(x, y - 1, visited)
        if self.board[y][x].right() and x + 1 < self.size and  self.board[y][x + 1].left():
            reachable += self._reachable_from_help(x + 1, y, visited)
        if self.board[y][x].down() and y + 1 < self.size and self.board[y + 1][x].up():
            reachable += self._reachable_from_help(x, y + 1, visited)
        if self.board[y][x].left() and x - 1 >= 0 and self.board[y][x - 1].right():
            reachable += self._reachable_from_help(x - 1, y, visited)
        return reachable

def visit(protoboard: List[List[ProtoTile]], x: int, y: int) -> bool:
    if x < 0 or x >= len(protoboard) or y < 0 or y >= len(protoboard):
        return False
    if protoboard[y][x].visited:
        return False
    # print("Visit ({}, {})".format(x, y))
    protoboard[y][x].visited = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(dirs)
    for (dx, dy) in dirs:
        if visit(protoboard, x + dx, y + dy):
            if dx == -1 and dy == 0:
                protoboard[y][x].left = True
                protoboard[y + dy][x + dx].right = True
            elif dx == 1 and dy == 0:
                protoboard[y][x].right = True
                protoboard[y + dy][x + dx].left = True
            elif dx == 0 and dy == -1:
                protoboard[y][x].up = True
                protoboard[y + dy][x + dx].down = True
            else:
                protoboard[y][x].down = True
                protoboard[y + dy][x + dx].up = True
    return True