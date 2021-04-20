from vector import Vector3
from Mesh import Mesh
from Object import Object

class Triangle(Object):
    def __init__(self, p1:Vector3, p2:Vector3, p3:Vector3, color=['blue']):
        self.bilateral = False
        vertices = [p1, p2, p3]
        self.mesh = Mesh(vertices, [0, 1, 2], [color])
        super().__init__(self.mesh.centroids[0], Vector3(1,1,1), Vector3(0,0,0))

    def setBilateral(self, b:bool):
        self.bilateral = b
        if b:
            self.mesh = Mesh(self.mesh.vertices, [0,1,2, 0,2,1], [self.mesh.color[0] for _ in range(2)])
