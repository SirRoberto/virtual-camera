import numpy as np

class Vector2():
    def __init__(self, x, y):
        self.vec = np.array([x, y, 1])
    
    def getX(self):
        return self.vec[0]
        
    def getY(self):
        return self.vec[1]

    def setX(self, x):
        self.vec[0] = x
        
    def setY(self, y):
        self.vec[1] = y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return self.vec + other.vec

    def __sub__(self, other):
        if isinstance(other, Vector2):
            return self.vec - other.vec

    def __eq__(self, other):
        if isinstance(other, Vector3):
            return (self.getX() == other.getX() and 
                    self.getY() == other.getY())

    def __str__(self):
        return f"Vector2: ({self.getX()}, {self.getY()})"


class Vector3():
    def __init__(self, x, y, z):
        self.vec = np.array([x, y, z, 1], dtype=float)
    
    def getX(self):
        return self.vec[0]
        
    def getY(self):
        return self.vec[1]

    def getZ(self):
        return self.vec[2]

    def setX(self, x):
        self.vec[0] = x
        
    def setY(self, y):
        self.vec[1] = y

    def setZ(self, z):
        self.vec[2] = z

    def setVec(self, v):
        self.vec = vec

    def negative(self):
        return Vector3(-self.getX(), -self.getY(), -self.getZ())

    def __add__(self, other):
        if isinstance(other, Vector3):
            v = self.vec + other.vec
            return Vector3(v[0],v[1],v[2])

    def __sub__(self, other):
        if isinstance(other, Vector3):
            v = self.vec - other.vec
            return Vector3(v[0],v[1],v[2])

    def __neg__(self):
        v = - self.vec
        return Vector3(v[0],v[1],v[2])

    def __mul__(self, other):
        if isinstance(other, Vector3):
            v = self.vec * other.vec
            return Vector3(v[0],v[1],v[2])
        elif isinstance(other, float) or isinstance(other, int):
            v = self.vec * other
            return Vector3(v[0],v[1],v[2])

    def __eq__(self, other):
        if isinstance(other, Vector3):
            return (self.getX() == other.getX() and 
                    self.getY() == other.getY() and 
                    self.getZ() == other.getZ())

    def __str__(self):
        return f"({round(self.getX(),5)}, {round(self.getY(),5)}, {round(self.getZ(),5)})"


if __name__ == '__main__':
    print(-Vector3(1,2,3))