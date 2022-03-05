from enum import IntEnum

class ProtoTile:
    def __init__(self):
        self.up = False
        self.right = False
        self.down = False
        self.left = False
        self.visited = False

class Tile:
    rotation = 0
    MAX_ROTATION: int

    @staticmethod
    def from_prototile(prototile: ProtoTile) -> 'Tile':
        sides = prototile.up + prototile.down + prototile.left + prototile.right
        if sides == 3:
            if not prototile.up: return SplitPipe(SplitPipe.Orient.DOWN)
            if not prototile.down: return SplitPipe(SplitPipe.Orient.UP)
            if not prototile.left: return SplitPipe(SplitPipe.Orient.RIGHT)
            if not prototile.right: return SplitPipe(SplitPipe.Orient.LEFT)
        elif sides == 2:
            if prototile.up and prototile.down: return LongPipe(LongPipe.Orient.VERTICAL)
            if prototile.left and prototile.right: return LongPipe(LongPipe.Orient.HORIZONTAL)
            if prototile.up and prototile.left: return CornerPipe(CornerPipe.Orient.TOP_LEFT)
            if prototile.up and prototile.right: return CornerPipe(CornerPipe.Orient.TOP_RIGHT)
            if prototile.down and prototile.left: return CornerPipe(CornerPipe.Orient.BOTTOM_LEFT)
            if prototile.down and prototile.right: return CornerPipe(CornerPipe.Orient.BOTTOM_RIGHT)
        elif sides == 1:
            if prototile.up: return EndPipe(EndPipe.Orient.UP)
            if prototile.down: return EndPipe(EndPipe.Orient.DOWN)
            if prototile.left: return EndPipe(EndPipe.Orient.LEFT)
            if prototile.right: return EndPipe(EndPipe.Orient.RIGHT)

        raise Exception("{} sides is illegal".format(sides))

    def rotate(self):
        self.rotation += 1
        self.rotate_right()

    def rotate_right(self) -> None:
        raise NotImplementedError()

    def up(self) -> bool:
        raise NotImplementedError()

    def down(self) -> bool:
        raise NotImplementedError()

    def left(self) -> bool:
        raise NotImplementedError()

    def right(self) -> bool:
        raise NotImplementedError()

class EndPipe(Tile):
    class Orient(IntEnum):
        UP = 0
        LEFT = 1
        DOWN = 2
        RIGHT = 3

    def __init__(self, orient: Orient):
        self.orient = orient
        self.MAX_ROTATION = 4

    def rotate_right(self):
        self.orient = (self.orient + 1) % 4

    def up(self) -> bool:
        return self.orient == self.Orient.UP

    def down(self) -> bool:
        return self.orient == self.Orient.DOWN

    def left(self) -> bool:
        return self.orient == self.Orient.LEFT

    def right(self) -> bool:
        return self.orient == self.Orient.RIGHT

class LongPipe(Tile):
    class Orient(IntEnum):
        VERTICAL = 0
        HORIZONTAL = 1
    def __init__(self, orient: Orient):
        self.orient = orient
        self.MAX_ROTATION = 2

    def rotate_right(self):
        self.orient = 1 - self.orient

    def up(self) -> bool:
        return self.orient == self.Orient.VERTICAL

    def down(self) -> bool:
        return self.orient == self.Orient.VERTICAL

    def left(self) -> bool:
        return self.orient == self.Orient.HORIZONTAL

    def right(self) -> bool:
        return self.orient == self.Orient.HORIZONTAL

class CornerPipe(Tile):
    class Orient(IntEnum):
        TOP_LEFT = 0
        TOP_RIGHT = 1
        BOTTOM_RIGHT = 2
        BOTTOM_LEFT = 3

    def __init__(self, orient: Orient):
        self.orient = orient
        self.MAX_ROTATION = 4

    def rotate_right(self):
        self.orient = (self.orient + 1) % 4

    def up(self) -> bool:
        # 0 or 1
        return self.orient // 2 == 0

    def down(self) -> bool:
        # 2 or 3
        return self.orient // 2 == 1

    def left(self) -> bool:
        # 0 or 3
        return ((self.orient + 1) % 4) // 2 == 0

    def right(self) -> bool:
        # 1 or 2
        return ((self.orient + 1) % 4) // 2 == 1

class SplitPipe(Tile):
    class Orient(IntEnum):
        UP = 0
        LEFT = 1
        DOWN = 2
        RIGHT = 3

    def __init__(self, orient: Orient):
        self.orient = orient
        self.MAX_ROTATION = 4

    def rotate_right(self):
        self.orient = (self.orient + 1) % 4

    def up(self) -> bool:
        return self.orient != self.Orient.DOWN

    def down(self) -> bool:
        return self.orient != self.Orient.UP

    def left(self) -> bool:
        return self.orient != self.Orient.RIGHT

    def right(self) -> bool:
        return self.orient != self.Orient.LEFT