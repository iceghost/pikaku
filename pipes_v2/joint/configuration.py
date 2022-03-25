from copy import copy

from pipes_v2.joint import Joint


class JointConfiguration:
    """
    Abstraction for top - right - bottom - left configuration.
    """

    def __init__(
        self,
        top: Joint = Joint.UNKNOWN,
        right: Joint = Joint.UNKNOWN,
        bottom: Joint = Joint.UNKNOWN,
        left: Joint = Joint.UNKNOWN,
    ) -> None:
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

    CHARSET = "?╡╥╗╞═╔╦╨╝║╣╚╩╠?"
    CHARSET_DICT = {v: i for (i, v) in enumerate(CHARSET)}

    @staticmethod
    def from_str(raw: str):
        index = JointConfiguration.CHARSET_DICT[raw]
        return JointConfiguration(
            Joint(index // 8),
            Joint((index % 8) // 4),
            Joint((index % 4) // 2),
            Joint(index % 2),
        )

    def __str__(self) -> str:
        if any(joint == Joint.UNKNOWN for joint in self.joints()):
            return "?"
        char = JointConfiguration.CHARSET[
            8 * self.top + 4 * self.right + 2 * self.bottom + self.left
        ]
        if char is not None:
            return char
        raise IndexError

    def rotate_right(self) -> "JointConfiguration":
        other = copy(self)
        other.top, other.right, other.bottom, other.left = (
            other.left,
            other.top,
            other.right,
            other.bottom,
        )
        return other

    def is_fit_into(self, config: "JointConfiguration"):
        return (
            self.top.is_fit_to(config.top)
            and self.right.is_fit_to(config.right)
            and self.bottom.is_fit_to(config.bottom)
            and self.left.is_fit_to(config.left)
        )

    def joints(self):
        return [self.top, self.right, self.bottom, self.left]

    def __getitem__(self, key):
        if key == 0:
            return self.top
        elif key == 1:
            return self.right
        elif key == 2:
            return self.bottom
        elif key == 3:
            return self.left
        raise KeyError

    def __setitem__(self, key, value: Joint):
        if key == 0:
            self.top = value
        elif key == 1:
            self.right = value
        elif key == 2:
            self.bottom = value
        elif key == 3:
            self.left = value
        raise KeyError
