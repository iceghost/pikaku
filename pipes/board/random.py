from typing import List
from . import Board
from .tiles import ProtoTile, Tile
from random import randrange, shuffle


def visit(protoboard: List[List[ProtoTile]], x: int, y: int, visited: List[List[bool]]) -> bool:
    if x < 0 or x >= len(protoboard[0]) or y < 0 or y >= len(protoboard):
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


def random(height: int, width: int) -> 'Board':
    protoboard = [[ProtoTile() for _ in range(0, width)]
                  for _ in range(0, height)]
    visited = [[False] * width for _ in range(0, height)]
    visit(protoboard, 0, 0, visited)

    board = Board([[rotate(Tile.from_prototile(col)) for col in row]
                   for row in protoboard])
    return board


def rotate(tile: Tile):
    step = randrange(0, tile.MAX_ROTATION)
    if step == 0: return tile
    return tile.rotate(step)