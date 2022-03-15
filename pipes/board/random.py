from typing import List
from . import Board
from .tiles import ProtoTile, Tile
from random import randrange, shuffle

def visit(protoboard: List[List[ProtoTile]], x: int, y: int, visited: List[List[bool]]) -> bool:
    if x < 0 or x >= len(protoboard) or y < 0 or y >= len(protoboard):
        return False
    if visited[y][x]:
        return False
    # print("Visit ({}, {})".format(x, y))
    visited[y][x] = True
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    shuffle(dirs)
    for (dx, dy) in dirs:
        if visit(protoboard, x + dx, y + dy, visited):
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

def random(size: int) -> 'Board':
    protoboard = [[ProtoTile() for _ in range(0, size)]
                    for _ in range(0, size)]
    visited = [[False] * size for _ in range(0, size)]
    visit(protoboard, 0, 0, visited)
    board = Board([[Tile.from_prototile(col) for col in row]
                    for row in protoboard])
    for x in range(0, len(board)):
        for y in range(0, len(board)):
            tile = board.at(x, y)
            for _ in range(0, randrange(0, tile.max_rotation - 1)):
                board.rotate(x, y)
    return board