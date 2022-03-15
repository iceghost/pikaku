from pipes.agent import blind_search
from pipes.board.random import random as brandom
from pipes.board.tiles import ProtoTile, Tile

if __name__ == "__main__":
    tile = ProtoTile()
    tile.up = True
    tile.down = True
    tile.right = True
    tile = Tile.from_prototile(tile)

    print(tile)

    board = brandom(3)

    print(board)
    print("\n")
    blind_search(board)
    print(board)
    print("\n")
    print(board.is_solved())
    print(len(board))
