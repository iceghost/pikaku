from board import Board
from agent import blind_search
from tile import ProtoTile, Tile

tile = ProtoTile()
tile.up = True
tile.down = True
tile.right = True
tile = Tile.from_prototile(tile)

print(tile)

board = Board.random(3)

print(board)
print("\n")
blind_search(board)
print(board)
print("\n")
print(board.is_solved())
print(len(board))