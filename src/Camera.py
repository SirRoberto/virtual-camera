from Object import Object
from vector import Vector3
from Projection import PerspectiveProjection
from Controler import Controler
from Mesh import Mesh
from math import tan, radians

class Camera(Object, PerspectiveProjection):
    def __init__(self, location:Vector3, dimension:Vector3, rotation:Vector3, fov):
        super().__init__(location, dimension, rotation)
        self.fov = fov
        self.d = self.__calc_vpd(fov)
        self.controler = Controler(self)


    def projectObject(self, mesh:Mesh):
        self.d = self.__calc_vpd(self.fov)
        return super().projectObject(mesh, self.location, self.rotation, self.d)
        

    def __calc_vpd(self, fov):
        return 0.5 * self.dimension.getX() / tan(radians(fov/2))


    def setWidth(self, v):
        self.dimension.setX(v)
        self.vpd = self.__calc_vpd(self.fov)
        
    def setHeigth(self, v):
        self.dimension.setY(v)
        self.vpd = self.__calc_vpd(self.fov)

    def setFOV(self, fov):
        self.fov = fov
        self.vpd = self.__calc_vpd(fov)





    

