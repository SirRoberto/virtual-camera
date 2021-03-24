from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from Cuboid import Cuboid
from Camera import Camera
from utils import Painter, importObjects

from vector import Vector3

SIZE_X = 800
SIZE_Y = 600

class Scene(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.interface()
        self.camera = Camera(Vector3(0,10,0), Vector3(self.width(),self.height(),0), Vector3(0,0,0), 90)
        self.objects = self.createObjects()
        self.keylist = []


    def interface(self):
        self.resize(SIZE_X, SIZE_Y)
        self.setWindowTitle("Wirtualna kamera")
        self.setStyleSheet("background-color: black;")


    def createObjects(self):
        return importObjects("objects.txt")


    def paintEvent(self, event):
        painter = Painter(self)
        self.camera.setWidth(self.width())
        self.camera.setHeigth(self.height())

        for o in self.objects:
            lines = self.camera.projectObject(o.mesh)
            painter.drawLines(lines)

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




