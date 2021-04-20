from vector import Vector3

class Controler():
    def __init__(self, camera):
        self.mode = True
        self.camera = camera
        self.delta = 1
        self.panel = {
            ord('W') : lambda : self.translateCamera(camera.transform.forward(), self.delta),
            ord('S') : lambda : self.translateCamera(camera.transform.back(), self.delta),
            ord('Q') : lambda : self.translateCamera(camera.transform.up(), self.delta),
            ord('E') : lambda : self.translateCamera(camera.transform.down(), self.delta),
            ord('D') : lambda : self.translateCamera(camera.transform.right(), self.delta),
            ord('A') : lambda : self.translateCamera(camera.transform.left(), self.delta),

            ord('R') : lambda : self.rotateCamera(camera.transform.left(), 0.5*self.delta),
            ord('T') : lambda : self.rotateCamera(camera.transform.right(), 0.5*self.delta),
            ord('F') : lambda : self.rotateCamera(camera.transform.down(), 0.5*self.delta),
            ord('G') : lambda : self.rotateCamera(camera.transform.up(), 0.5*self.delta),
            ord('V') : lambda : self.rotateCamera(camera.transform.back(), 0.5*self.delta),
            ord('B') : lambda : self.rotateCamera(camera.transform.forward(), 0.5*self.delta),

            ord('[') : lambda : self.zoom(1),
            ord(']') : lambda : self.zoom(-1),

            ord('+') : lambda : self.speed(2),
            ord('-') : lambda : self.speed(0.5),

            ord('.') : lambda : self.change_mode()
        }


    def translateCamera(self, v:Vector3, delta=1):
        self.camera.transform.translate(v, delta)


    def rotateCamera(self, v:Vector3, delta):
        self.camera.transform.rotate(v, delta)


    def zoom(self, d):
        if self.camera.fov > 10 and d < 0:
            self.camera.setFOV(self.camera.fov + d)
        elif self.camera.fov < 170 and d > 0:
            self.camera.setFOV(self.camera.fov + d)


    def speed(self, d):
        self.delta *= d


    def change_mode(self):
        self.mode = not self.mode