from vector import *
from Mesh import Mesh
from Object import Object
from Transformation import translate, rotateVectorAboutCenter
import numpy as np

class PerspectiveProjection():

    def projectPolygons(self, polygons, pos:Vector3, rot:Vector3, d):
        projected_polygons = []
        for polygon in polygons:
            if not self.__is_visible(polygon[-2], polygon[0], pos.vec[:3]):
                continue
            projected_points = []
            for point in polygon[:-2]:
                point = Vector3(point[0], point[1], point[2])
                point = self.__projectPoint(point, pos, rot, d)
                projected_points.append(point)
            projected_points.append(polygon[-1])
            projected_polygons.append(projected_points)

        return projected_polygons


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
        P = P / P[-1,-1]

        return Vector2(P[0,0], P[0,1])


    def __is_visible(self, n_p, p_p, pos):
        v = p_p - pos
        x = (v/np.linalg.norm(v)).dot(n_p/np.linalg.norm(n_p))
        return True if x > 0 else False
