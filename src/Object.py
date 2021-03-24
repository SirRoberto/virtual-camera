from vector import Vector3
from Transformation import Transformation

class Object():
    def __init__(self, location : Vector3, dimension : Vector3, rotation : Vector3):
        self.location = location
        self.dimension = dimension
        self.rotation = rotation
        self.transform = Transformation(self)

    def setLocation(self, v:Vector3):
        self.location = v

    def setDimension(self, v:Vector3):
        self.dimension = v

    def setRotation(self, v:Vector3):
        self.rotation = v
