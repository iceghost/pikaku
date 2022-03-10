from copy import copy


class ProtoTile:
    def __init__(self):
        self.up = False
        self.right = False
        self.down = False
        self.left = False

    def rotate_right(self):
        self.up, self.right, self.down, self.left = self.left, self.up, self.right, self.down


class Tile(ProtoTile):
    @staticmethod
    def from_prototile(prototile: ProtoTile) -> 'Tile':
        return Tile(**prototile.__dict__)

    def __init__(self,
                 up: bool,
                 right: bool,
                 down: bool,
                 left: bool,
                 ):
        sides = up + right + down + left
        if sides == 0 or sides == 4:
            raise Exception("{} sides is illegal".format(sides))
        self.up = up
        self.right = right
        self.down = down
        self.left = left
        if self.up and self.down:
            self.max_rotation = 2
        elif self.left and self.right:
            self.max_rotation = 2
        else:
            self.max_rotation = 4

    def __str__(self) -> str:
        sides = self.up + self.down + self.left + self.right
        if sides == 3:
            if not self.up:
                return "╦"
            elif not self.down:
                return "╩"
            elif not self.left:
                return "╠"
            else:  # not self.right:
                return "╣"
        elif sides == 2:
            if self.up and self.down:
                return "║"
            elif self.left and self.right:
                return "═"
            elif self.up and self.left:
                return "╝"
            elif self.up and self.right:
                return "╚"
            elif self.down and self.left:
                return "╗"
            else:  # self.down and self.right:
                return "╔"
        else:  # sides == 1
            if self.up:
                return "╨"
            elif self.down:
                return "╥"
            elif self.left:
                return "╡"
            else:  # self.right
                return "╞"

    def rotate(self, step: int = 1) -> 'Tile':
        other = copy(self)
        for _ in range(0, step % other.max_rotation):
            other.rotate_right()
        return other

    def rotate_right(self):
        self.up, self.right, self.down, self.left = self.left, self.up, self.right, self.down
