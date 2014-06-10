import numpy
import math
from pyul import coreUtils

__all__ = ['Quaternion']

class Quaternion(object):
    """
    This class represents a quaternion implemented using numpy arrays.
    """

    def __init__(self, w, x, y, z):
        """
        Creates a quaternion.

        """
        coreUtils.synthesize(self, 'data', numpy.array([w, x, y, z], dtype = numpy.float32))

    def __iadd__(self, q):
        """
        Adds a quaternion to this instance. Returns a reference to this
        instance.

        """
        self._data = numpy.add(self._data, q._data)
        return self

    def __isub__(self, q):
        """
        Subtracts a quaternion from this instance. Returns a reference to this
        instance.

        """
        self._data = numpy.subtract(self._data, q._data)
        return self

    def __imul__(self, q):
        """
        Post-multiplies this quaternion by another quaternion and returned a
        reference to this instance.

        """
        # (ur + ui)(vr + vi) = (ur * vr - ui * vi) + ur * vi + vr * ui + ui x vi

        u = self._data
        v = q._data

        r = u[0] * v[0] - numpy.dot(u[1:], v[1:])
        s = u[0] * v[1:] + v[0] * u[1:] + numpy.cross(u[1:], v[1:])

        self._data[0] = r
        self._data[1:] = s

        return self

    def __add__(self, q):
        """
        Adds a quaternion to this quaternion and returns the result.

        """
        r = self.clone()
        r += q
        return r

    def __sub__(self, q):
        """
        Subtracts a quaternion from this quaternion and returns the result.

        """
        r = self.clone()
        r -= q
        return r

    def __mul__(self, q):
        """
        Post-multiplies this quaternion by a another quaternion and results the
        result.

        """
        r = self.clone()
        r *= q
        return r

    def __eq__(self, q):
        """
        Returns True if the provided quaternion is equal to this quaternion.

        """
        return numpy.array_equal(self._data, q._data)

    def __ne__(self, q):
        """
        Returns False if the provided quaternion is equal to this quaternion.

        """
        return not numpy.array_equal(self._data, q._data)

    def __repr__(self):
        return repr((self.w, self.x, self.y, self.z))

    @property
    def w(self):
        """
        The w component of the quaternion.

        """
        return self._data[0]

    @property
    def x(self):
        """
        The x component of the quaternion.

        """
        return self._data[1]

    @property
    def y(self):
        """
        The y component of the quaternion.

        """
        return self._data[2]

    @property
    def z(self):
        """
        The z component of the quaternion.

        """
        return self._data[3]

    @property
    def length(self):
        """
        The length of the quaternion.

        """
        return numpy.linalg.norm(self._data)

    @classmethod
    def from_axis_angle(cls, axis, angle):
        """
        Creates an instance of Quaternion using an axis (unit vector) and an
        angle (radians).

        """
        lensqr = numpy.dot(axis, axis)
        if abs(lensqr - 1.0) > 0.0001:
            axis = axis / math.sqrt(lensqr)

        c = math.cos(angle / 2.0)
        s = math.sin(angle / 2.0)
        return cls(c, s * axis[0], s * axis[1], s * axis[2])

    def clone(self):
        """
        Returns a copy of this quaternion.

        """
        return Quaternion(self.w, self.x, self.y, self.z)

    def conjugate(self):
        """
        Conjugates this quaternion and returns a reference to this instance.

        """
        self._data[1:] = -self._data[1:]
        return self

    def invert(self):
        """
        Inverts this quaternion and returns a reference to this instance.

        """
        self.conjugate()
        self._data = self._data / numpy.dot(self._data, self._data)
        return self

    def normalize(self):
        """
        Normalizes this quaternion and returns a reference to this instance.

        """
        self._data = self._data / self.length
        return self

    def conjugated(self):
        """
        Returns a conjugates copy of this quaternion.

        """
        return self.clone().conjugate()

    def inverted(self):
        """
        Returns an inverted copy of this quaternion.

        """
        return self.clone().invert()

    def normalized(self):
        """
        Returns a normalized copy of this quaternion.

        """
        return self.clone().normalize()

    def angle(self):
        """
        Returns the angle that this quaternion represents (assumes that this is
        a unit quaternion).

        """
        return 2.0 * math.atan2(numpy.linalg.norm(self._data[1:]), self.w)

    def axis(self):
        """
        Returns the axis that this quaternion represents (assumes that this is a
        unit quaternion).

        """
        s2 = abs((1.0 - self.w) * (1.0 + self.w))
        if s2 < 0.000001:
            # When s2 is effectively zero, the angle of the quaternion is
            # approximately zero, so the axis returned is arbitrary.
            x = 0
            y = 0
            z = 1
        else:
            norm = numpy.linalg.norm(self._data[1:])
            x = self.x / norm
            y = self.y / norm
            z = self.z / norm

        return (x, y, z)

    def matrix(self):
        """
        Returns a matrix representation of the quaternion.

        """
        w = self.w
        x = self.x
        y = self.y
        z = self.z

        R = numpy.zeros((3,3))
        R[0,0] = 1.0 - 2.0 * (y * y + z * z)
        R[1,1] = 1.0 - 2.0 * (x * x + z * z)
        R[2,2] = 1.0 - 2.0 * (x * x + y * y)
        R[0,1] = 2.0 * (x * y + w * z)
        R[0,2] = 2.0 * (x * z - w * y)
        R[1,2] = 2.0 * (y * z + w * x)
        R[1,0] = 2.0 * (x * y - w * z)
        R[2,0] = 2.0 * (x * z + w * y)
        R[2,1] = 2.0 * (y * z - w * x)

        return R

    def rotate(self, (x, y, z)):
        """
        Rotates a vector by this quaternion and returns the result.

        """
        q = self * Quaternion(0, x, y, z) * self.inverted()
        return map(float, q.axis())
