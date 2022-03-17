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

    # top - right - bottom - left
    CHARSET = [
        None,
        "╡",
        "╥",
        "╗",
        "╞",
        "═",
        "╔",
        "╦",
        "╨",
        "╝",
        "║",
        "╣",
        "╚",
        "╩",
        "╠",
        None,
    ]

    CHARSET_DICT = {v: i for (i, v) in enumerate(CHARSET) if v is not None}

    @staticmethod
    def from_str(raw: str):
        index = Tile.CHARSET_DICT[raw]
        return Tile(index // 8, (index % 8) // 4, (index % 4) // 2, index % 2)  # type: ignore

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
        if sides == 2 and self.up and self.down:
            self.MAX_ROTATION = 2
        elif sides == 2 and self.left and self.right:
            self.MAX_ROTATION = 2  # type:ignore
        else:
            self.MAX_ROTATION = 4  # type:ignore

    def __str__(self) -> str:
        char = Tile.CHARSET[8 * self.up + 4 *
                            self.right + 2 * self.down + self.left]
        if char is not None:
            return char
        raise IndexError

    def __repr__(self) -> str:
        return "Tile({}, {}, {}, {})".format(self.up, self.right, self.down, self.left)

    def rotate(self, step: int = 1) -> 'Tile':
        other = copy(self)
        other.rotate_right(step)
        return other

    def rotate_right(self, step: int = 1):
        if step <= 0 or step >= self.MAX_ROTATION:
            raise Exception("cannot rotate {} steps".format(step))
        if step == 1:
            self.up, self.right, self.down, self.left = self.left, self.up, self.right, self.down
        elif step == 2:
            self.up, self.right, self.down, self.left = self.down, self.left, self.up, self.right
        elif step == 3:
            self.up, self.right, self.down, self.left = self.right, self.down, self.left, self.up
