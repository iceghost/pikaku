import numpy

from pipes_v2.joint import Joint
from pipes_v2.joint.configuration import JointConfiguration
from pipes_v2.utils.direction import dir_to_dx_dy


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

    def set_joint(self, x: int, y: int, dir: int, joint: Joint):
        """
        Set the joint in dir direction. Returns boolean indicating if
        anything changed.

        Ignore unknown joint.
        """
        if joint.is_unknown():
            return False
        dx, dy = dir_to_dx_dy(dir)
        if dx == 0:
            # scale -1,1 to 0,1
            dy = (dy + 1) // 2
            if self.h_joints[y + dy, x] != joint:
                self.h_joints[y + dy, x] = joint
                return True
        else:
            dx = (dx + 1) // 2
            if self.v_joints[y, x + dx] != joint:
                self.v_joints[y, x + dx] = joint
                return True
        return False

    def set(self, x: int, y: int, config: JointConfiguration):
        for dir, joint in enumerate(config.joints()):
            if self.set_joint(x, y, dir, joint):
                self.unknowns -= 1
