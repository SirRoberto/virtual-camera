from Object import Object
from vector import Vector3
from Mesh import Mesh

class Cuboid(Object):
    def __init__(self, location:Vector3, dimension:Vector3, rotation:Vector3):
        super().__init__(location, dimension, rotation)
        edges = [
            0, 1,   1, 2,   2, 3,   3, 0,
            4, 5,   5, 6,   6, 7,   7, 4,
            0, 4,   1, 5,   2, 6,   3, 7]
        self.mesh = Mesh(self.__calc_vertices(location, dimension), edges)


    def __calc_vertices(self, location, dimension):
        vertices = [
            Vector3(location.getX() - dimension.getX()/2,
                    location.getY() - dimension.getY()/2,
                    location.getZ() - dimension.getZ()/2),
            
            Vector3(location.getX() + dimension.getX()/2,
                    location.getY() - dimension.getY()/2,
                    location.getZ() - dimension.getZ()/2),

            Vector3(location.getX() + dimension.getX()/2,
                    location.getY() + dimension.getY()/2,
                    location.getZ() - dimension.getZ()/2),

            Vector3(location.getX() - dimension.getX()/2,
                    location.getY() + dimension.getY()/2,
                    location.getZ() - dimension.getZ()/2),

            Vector3(location.getX() - dimension.getX()/2,
                    location.getY() - dimension.getY()/2,
                    location.getZ() + dimension.getZ()/2),

            Vector3(location.getX() + dimension.getX()/2,
                    location.getY() - dimension.getY()/2,
                    location.getZ() + dimension.getZ()/2),

            Vector3(location.getX() + dimension.getX()/2,
                    location.getY() + dimension.getY()/2,
                    location.getZ() + dimension.getZ()/2),

            Vector3(location.getX() - dimension.getX()/2,
                    location.getY() + dimension.getY()/2,
                    location.getZ() + dimension.getZ()/2)
        ]
        return vertices


