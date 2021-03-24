from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import QWidget
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
        self.setRenderHint(QPainter.RenderHints.Antialiasing)

    def drawLine(self, line):
        point1 = line[0]
        point2 = line[1]
        x1 = self.evaluate(line[0].getX() + self.widget.width()/2)
        y1 = self.evaluate(-line[0].getY() + self.widget.height()/2)
        x2 = self.evaluate(line[1].getX() + self.widget.width()/2)
        y2 = self.evaluate(-line[1].getY() + self.widget.height()/2)
        super().drawLine(x1, y1, x2, y2)

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
    objects = []
    with open(os.path.join(__location__, filePath), "r") as inFile:
        lines = inFile.read().splitlines()
        for line in lines:
            if (len(line) > 0) and (line[0] != '#'):
                name, parameters = line.split('(', 1)
                name = name.strip()
                parameters = parameters.strip()[:-1]
                if(name == 'Cuboid'):
                    parameters = re.findall(r"\([ -]*\d+ *\,[ -]*\d+ *\,[ -]*\d+ *\)", parameters)
                    try:
                        position, dimension = parameters[0], parameters[1]
                        position = re.findall(r"-*\w+", position)
                        dimension = re.findall(r"-*\w+", dimension)
                        position = [float(x) for x in position]
                        dimension = [float(x) for x in dimension]
                        try:
                            objects.append(Cuboid(
                                Vector3(position[0], position[1], position[2]),
                                Vector3(dimension[0], dimension[1], dimension[2]),
                                Vector3(0,0,0)
                            ))
                        except:
                            raise Exception("Niepowodzenie utworzenia obiektu")
                    except Exception as err:
                        raise Exception(err)
                else:
                    raise Exception("Figura o podanej nazwie nie istnieje")
    return objects
