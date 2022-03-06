import random
from typing import List
from tile import ProtoTile, Tile


class Board:
    def __init__(self, board: List[List[Tile]]):
        self.board = board

    @staticmethod
    def random(size: int) -> 'Board':
        protoboard = [[ProtoTile() for _ in range(0, size)] for _ in range(0, size)]
        visit(protoboard, 0, 0)
        return Board([[Tile.from_prototile(col) for col in row] for row in protoboard])

    def __str__(self) -> str:
        return "\n".join(["".join([col.to_char() for col in row]) for row in self.board])

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
    for _ in range(0, random.randrange(0, 4)):
        protoboard[y][x].rotate_right()
    return True