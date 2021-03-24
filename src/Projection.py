from vector import *
from Mesh import Mesh
from Object import Object
from Transformation import translate, rotateVectorAboutCenter
import numpy as np

class PerspectiveProjection():

    def projectObject(self, mesh:Mesh, pos:Vector3, rot:Vector3, d):
        points_ = []
        for point in mesh.vertices:
            p_ = self.__projectPoint(point, pos, rot, d)
            vec = Vector2(p_[0,0], p_[0,1])
            points_.append(vec)

        lines = []
        for x, y in zip(mesh.edges[0::2], mesh.edges[1::2]):
            line = (points_[x], points_[y])
            lines.append(line)
        return lines


    def __projectPoint(self, point:Vector3, pos:Vector3, rot:Vector3, d):
        point = translate(point, -pos)
        point = rotateVectorAboutCenter(point, -rot)
        
        if point.getZ() < 0.001:
            point.setZ(0.001)
        
        M = np.matrix([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0,1/d,0]
        ])
        P = np.dot(M, point.vec)
        return P/P[-1,-1]
