from Object import Object
from vector import Vector3
from Mesh import Mesh

class Cuboid(Object):
    def __init__(self, location:Vector3, dimension:Vector3, rotation:Vector3, color=['blue']):
        super().__init__(location, dimension, rotation)
        triangles = [
                0,1,4, 1,5,4, 1,2,6, 1,6,5, 2,3,6, 3,7,6,
                3,0,4, 3,4,7, 4,5,6, 4,6,7, 0,3,1, 1,3,2]
        color = [color for _ in range(12)]
        self.mesh = Mesh(self.__calc_vertices(location, dimension), triangles, color)

    def __calc_vertices(self, location, dimension):
        vertices = [
            Vector3(location.getX() - dimension.getX()/2,
                    location.getY() - dimension.getY()/2,
                    location.getZ() - dimension.getZ()/2),
            
            Vector3(location.getX() + dimension.getX()/2,
                    location.getY() - dimension.getY()/2,
                    location.getZ() - dimension.getZ()/2),

            Vector3(location.getX() + dimension.getX()/2,
                    location.getY() - dimension.getY()/2,
                    location.getZ() + dimension.getZ()/2),

            Vector3(location.getX() - dimension.getX()/2,
                    location.getY() - dimension.getY()/2,
                    location.getZ() + dimension.getZ()/2),

            Vector3(location.getX() - dimension.getX()/2,
                    location.getY() + dimension.getY()/2,
                    location.getZ() - dimension.getZ()/2),

            Vector3(location.getX() + dimension.getX()/2,
                    location.getY() + dimension.getY()/2,
                    location.getZ() - dimension.getZ()/2),

            Vector3(location.getX() + dimension.getX()/2,
                    location.getY() + dimension.getY()/2,
                    location.getZ() + dimension.getZ()/2),

            Vector3(location.getX() - dimension.getX()/2,
                    location.getY() + dimension.getY()/2,
                    location.getZ() + dimension.getZ()/2)
        ]
        return vertices


