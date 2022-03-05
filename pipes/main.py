from tile import ProtoTile, Tile

tile = ProtoTile()
tile.up = True
tile.down = True
tile.right = True
tile = Tile.from_prototile(tile)

print(tile)