import numpy

from pipes_v2.joint import Joint
from pipes_v2.joint.configuration import JointConfiguration
from pipes_v2.utils.direction import dir_to_dx_dy


class JointMatrix:
    """Represent joints of a board."""

    def __init__(self, height: int, width: int):
        self.HEIGHT = height
        self.WIDTH = width

        # v for vertical, h for horizontal
        self.v_joints = numpy.full((height, width + 1), Joint.UNKNOWN, numpy.int8)
        self.h_joints = numpy.full((height + 1, width), Joint.UNKNOWN, numpy.int8)

        # initialize border for non-wrap pipe game
        self.v_joints[:, 0] = Joint.UNCONNECTED
        self.v_joints[:, -1] = Joint.UNCONNECTED
        self.h_joints[0, :] = Joint.UNCONNECTED
        self.h_joints[-1, :] = Joint.UNCONNECTED

    def __hash__(self) -> int:
        return hash((self.v_joints.tobytes(), self.h_joints.tobytes()))

    def __eq__(self, __o: "JointMatrix") -> bool:
        return numpy.array_equal(self.v_joints, __o.v_joints) and numpy.array_equal(
            self.h_joints, __o.h_joints
        )

    def at(self, x: int, y: int):
        top = self.h_joints[y, x]
        bottom = self.h_joints[y + 1, x]
        left = self.v_joints[y, x]
        right = self.v_joints[y, x + 1]
        return JointConfiguration(Joint(top), Joint(right), Joint(bottom), Joint(left))

    def is_solved_at(self, x: int, y: int):
        return not any(map(Joint.is_unknown, self.at(x, y).joints()))

    def set_joint(self, x: int, y: int, dir: int, joint: Joint):
        """Set the joint in dir direction.

        Ignore unknown joints.
        """
        if joint.is_unknown():
            return
        dx, dy = dir_to_dx_dy(dir)
        if dx == 0:
            # scale -1,1 to 0,1
            dy = (dy + 1) // 2
            self.h_joints[y + dy, x] = joint
        else:
            dx = (dx + 1) // 2
            self.v_joints[y, x + dx] = joint

    def set(self, x: int, y: int, config: JointConfiguration):
        """Set joints at position.

        Ignore unknown joints.
        """
        for dir, joint in enumerate(config.joints()):
            self.set_joint(x, y, dir, joint)

    def is_closed(self):
        """Check if every joint is closed.

        Use with iso-joints.
        """
        return (
            numpy.count_nonzero(self.h_joints) == 0
            and numpy.count_nonzero(self.v_joints) == 0
        )

    def count_unsolved(self):
        count = 0
        for y in range(0, self.HEIGHT):
            for x in range(0, self.WIDTH):
                if not self.is_solved_at(x, y):
                    count += 1
        return count

    def __str__(self):
        return "\n".join(
            [
                "".join([str(self.at(x, y)) for x in range(0, self.WIDTH)])
                for y in range(0, self.HEIGHT)
            ]
        )
