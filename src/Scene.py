from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from Cuboid import Cuboid
from Triangle import Triangle
from Camera import Camera
from SpacePartitioning import BinarySpacePartitioning
from utils import Painter, importObjects

from vector import Vector3

SIZE_X = 800
SIZE_Y = 600

class Scene(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interface()
        self.camera = Camera(Vector3(60,60,-100), Vector3(self.width(),self.height(),0), Vector3(0,0,0), 90)
        self.createObjects()
        self.determineVisibleSurface()
        self.keylist = []


    def interface(self):
        self.resize(SIZE_X, SIZE_Y)
        self.setWindowTitle("Wirtualna kamera")
        self.setStyleSheet("background-color: black;")


    def createObjects(self):
        #self.objects = importObjects("objects.txt")

        v = Vector3(-100,0,0)
        self.objects =[
            Triangle(Vector3(0,0,0)+v, Vector3(40,0,0)+v, Vector3(20,140,-10)+v, ['red']),
            Triangle(Vector3(-40,20,-10)+v, Vector3(100,0,0)+v, Vector3(100,40,0)+v, ['green']),
            Triangle(Vector3(60,100,0)+v, Vector3(80,-40,-10)+v, Vector3(100,100,0)+v, ['blue']),
            Triangle(Vector3(0,100,0)+v, Vector3(0,60,0)+v, Vector3(140,80,-10)+v, ['orange']),
        ]


    def determineVisibleSurface(self):
        self.partitioning = BinarySpacePartitioning(self.objects)


    def paintEvent(self, event):
        painter = Painter(self)
        self.camera.setWidth(self.width())
        self.camera.setHeigth(self.height())

        polygons = self.partitioning.getOrderedPolygons(self.camera.location)
        polygons = self.camera.projectObject(polygons)
        painter.drawPolygon(polygons)

        font = painter.font()
        font.setPixelSize(18)
        painter.setFont(font)
        painter.drawText(10,20,"Location: "+str(self.camera.location))
        painter.drawText(10,40,"Rotation: "+str(self.camera.rotation))
        painter.drawText(10,60,"View Angle: "+str(self.camera.fov))
        painter.drawText(10,80,"Speed: "+str(self.camera.controler.delta))

    
    def keyPressEvent(self, event):
        self.firstrelease = True
        self.keylist.append(event.key())

    def keyReleaseEvent(self, event):
        if self.firstrelease == True: 
            self.processmultikeys(self.keylist)
        self.firstrelease = False
        del self.keylist[-1]

    def processmultikeys(self,keyspressed):
        for key in keyspressed:
            try:
                self.camera.controler.panel[key]()
            except Exception as err:
                pass
        self.update()




