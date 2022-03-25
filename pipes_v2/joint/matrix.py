import numpy

from pipes_v2.joint import Joint
from pipes_v2.joint.configuration import JointConfiguration


class JointMatrix:
    def __init__(self, height: int, width: int):
        # v for vertical, h for horizontal
        self.v_joints = numpy.full((height, width + 1), Joint.UNKNOWN, numpy.int8)
        self.h_joints = numpy.full((height + 1, width), Joint.UNKNOWN, numpy.int8)

        # initialize border for non-wrap pipe game
        self.v_joints[:, 0] = Joint.UNCONNECTED
        self.v_joints[:, -1] = Joint.UNCONNECTED
        self.h_joints[0, :] = Joint.UNCONNECTED
        self.h_joints[-1, :] = Joint.UNCONNECTED

        self.unknowns = numpy.count_nonzero(self.v_joints) + numpy.count_nonzero(
            self.h_joints
        )

    def at(self, x: int, y: int):
        top = self.h_joints[y, x]
        bottom = self.h_joints[y + 1, x]
        left = self.v_joints[y, x]
        right = self.v_joints[y, x + 1]
        return JointConfiguration(Joint(top), Joint(right), Joint(bottom), Joint(left))

    def solved_at(self, x: int, y: int):
        config = self.at(x, y)
        return (
            config.top != Joint.UNKNOWN
            and config.bottom != Joint.UNKNOWN
            and config.left != Joint.UNKNOWN
            and config.right != Joint.UNKNOWN
        )

    def set(self, x: int, y: int, config: JointConfiguration):
        if config.top != Joint.UNKNOWN and config.top != self.h_joints[y, x]:
            self.h_joints[y, x] = config.top
            self.unknowns -= 1
        if config.bottom != Joint.UNKNOWN and config.bottom != self.h_joints[y + 1, x]:
            self.h_joints[y + 1, x] = config.bottom
            self.unknowns -= 1
        if config.left != Joint.UNKNOWN and config.left != self.v_joints[y, x]:
            self.v_joints[y, x] = config.left
            self.unknowns -= 1
        if config.right != Joint.UNKNOWN and config.right != self.v_joints[y, x + 1]:
            self.v_joints[y, x + 1] = config.right
            self.unknowns -= 1
