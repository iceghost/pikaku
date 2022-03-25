from enum import IntEnum


class Joint(IntEnum):
    UNKNOWN = -1
    UNCONNECTED = 0
    CONNECTED = 1

    def is_connected(self):
        return self is Joint.CONNECTED

    def is_unconnected(self):
        return self is Joint.UNCONNECTED

    def is_unknown(self):
        return self is Joint.UNKNOWN

    def is_fit_to(self, other: "Joint"):
        return self is other or self is Joint.UNKNOWN or other is Joint.UNKNOWN
