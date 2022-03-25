from enum import IntEnum


class Joint(IntEnum):
    UNKNOWN = -1
    UNCONNECTED = 0
    CONNECTED = 1

    def is_connected(self):
        return self == Joint.CONNECTED

    def is_unconnected(self):
        return self == Joint.UNCONNECTED

    def is_unknown(self):
        return self == Joint.UNKNOWN
