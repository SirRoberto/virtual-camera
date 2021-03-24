from vector import Vector3
from math import sin, cos, radians, sqrt, atan2, degrees, asin, pi
import numpy as np
import sys

class Transformation():
    def __init__(self, o):
        self.__o = o
        self.mRot = np.matrix([
            [1,0,0],
            [0,1,0],
            [0,0,1],
            [1,1,1]
        ])

    def forward(self):
        m = self.mRot
        return Vector3(m[0,2],m[1,2],m[2,2])

    def back(self):
        m = -self.mRot
        return Vector3(m[0,2],m[1,2],m[2,2])

    def up(self):
        m = self.mRot
        return Vector3(m[0,1],m[1,1],m[2,1])

    def down(self):
        m = -self.mRot
        return Vector3(m[0,1],m[1,1],m[2,1])

    def right(self):
        m = self.mRot
        return Vector3(m[0,0],m[1,0],m[2,0])

    def left(self):
        m = -self.mRot
        return Vector3(m[0,0],m[1,0],m[2,0])


    def translate(self, v:Vector3, delta=1):
        self.__o.setLocation(translate(self.__o.location, v, delta))


    def rotate(self, v:Vector3, delta=1):
        self.mRot = rotateMatrixAboutAxisByAngle(self.mRot, v, delta)
        x, y, z = rotationMatrixToEulerAngles(self.mRot)
        self.__o.setRotation(Vector3(degrees(x),degrees(y),degrees(z)))     


def translate(p:Vector3, u:Vector3, delta=1):
    tx = delta * u.getX()
    ty = delta * u.getY()
    tz = delta * u.getZ()

    M = np.matrix([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0,  1]
    ])

    v = M.dot(p.vec)
    return Vector3(v[0,0], v[0,1], v[0,2])


def rotateVectorAboutCenter(v:Vector3, r:Vector3):
    a = radians(r.getX())
    b = radians(r.getY())
    c = radians(r.getZ())

    mOX = np.matrix([
        [1,    0,     0,     0],
        [0, cos(a), -sin(a), 0],
        [0, sin(a),  cos(a), 0],
        [0,    0,     0,     1]
    ])

    mOY = np.matrix([
        [ cos(b), 0, sin(b), 0],
        [   0,    1,    0,   0],
        [-sin(b), 0, cos(b), 0],
        [   0,    0,    0,   1]
    ])

    mOZ = np.matrix([
        [cos(c), -sin(c), 0, 0],
        [sin(c),  cos(c), 0, 0],
        [  0,     0,    1,   0],
        [  0,     0,    0,   1]
    ])

    u = mOX * mOY * mOZ * np.matrix(v.vec).T
    return Vector3(u[0,0], u[1,0], u[2,0])


def rotateMatrixAboutAxisByAngle(v:np.matrix, u:Vector3, alpha=100):
    x = u.getX()
    y = u.getY()
    z = u.getZ()
    alpha = radians(alpha)
    S = sin(alpha)
    C = cos(alpha)
    t = 1 - C

    R = np.matrix([
        [t*x*x+C, t*x*y-S*z, t*x*z+S*y, 0],
        [t*x*y+S*z, t*y*y+C, t*y*z-S*x, 0],
        [t*x*z-S*y, t*y*z+S*x, t*z*z+C, 0],
        [0,         0,         0,       1]
    ])

    return R.dot(v)


def isclose(x, y, rtol=1.e-5, atol=1.e-8):
    return abs(x-y) <= atol + rtol * abs(y)

def rotationMatrixToEulerAngles(R):
    phi = 0.0
    if isclose(R[2,0],-1.0):
        theta = pi/2.0
        psi = atan2(R[0,1],R[0,2])
    elif isclose(R[2,0],1.0):
        theta = -pi/2.0
        psi = atan2(-R[0,1],-R[0,2])
    else:
        theta = -asin(R[2,0])
        cos_theta = cos(theta)
        psi = atan2(R[2,1]/cos_theta, R[2,2]/cos_theta)
        phi = atan2(R[1,0]/cos_theta, R[0,0]/cos_theta)
    return np.array([psi, theta, phi])
