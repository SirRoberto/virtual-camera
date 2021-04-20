from PyQt6.QtGui import QPainter, QColor, QPolygon, QPen
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPoint
from Cuboid import Cuboid
from vector import Vector3
import os
import re

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Painter(QPainter):
    def __init__(self, widget:QWidget):
        super().__init__(widget)
        self.widget = widget
        self.setPen(QColor('white'))
        self.setBrush(QColor('blue'))
        self.setRenderHint(QPainter.RenderHints.Antialiasing)

    def drawPolygon(self, polygons):
        for polygon in polygons:
            xy = []
            for p in polygon[:-1]:
                x = self.evaluate(p.getX() + self.widget.width()/2)
                y = self.evaluate(-p.getY() + self.widget.height()/2)
                xy.append(QPoint(x, y))
            self.setBrush(QColor(polygon[-1][0]))

            if self.widget.camera.controler.mode:
                self.setPen(QColor(polygon[-1][0]))
            else: 
                self.setPen(QColor('white'))

            super().drawPolygon(QPolygon(xy))
        self.setPen(QColor('white'))

    def drawLines(self, lines):
        for line in lines:
            self.drawLine(line)

    def evaluate(self, x):
        if abs(x) < 2147483647:
            return x
        elif x > 2147483647:
            return 2147483647
        else:
            return -2147483648


def importObjects(filePath: str):
    i = 0
    objects = []
    with open(os.path.join(__location__, filePath), "r") as inFile:
        lines = inFile.read().splitlines()
        for line in lines:
            if (len(line) > 0) and (line[0] != '#'):
                name, parameters = line.split('(', 1)
                name = name.strip()
                parameters = parameters.strip()[:-1]
                if(name == 'Cuboid'):
                    p = re.findall(r"\([ -]*\d+ *\,[ -]*\d+ *\,[ -]*\d+ *\)", parameters)
                    color = str(re.findall(r"[a-zA-Z]+", parameters)[0])
                    try:
                        position, dimension = p[0], p[1]
                        position = re.findall(r"-*\w+", position)
                        dimension = re.findall(r"-*\w+", dimension)
                        position = [float(x) for x in position]
                        dimension = [float(x) for x in dimension]
                        try:
                            objects.append(Cuboid(
                                Vector3(position[0], position[1], position[2]),
                                Vector3(dimension[0], dimension[1], dimension[2]),
                                Vector3(0,0,0),
                                [color]
                            ))
                            i += 1
                        except:
                            raise Exception("Niepowodzenie utworzenia obiektu")
                    except Exception as err:
                        raise Exception(err)
                else:
                    raise Exception("Figura o podanej nazwie nie istnieje")
    return objects
