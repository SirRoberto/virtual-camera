import numpy as np
from vector import Vector3

class Mesh():
    def __init__(self, vertices, triangles, color):
        self.vertices = vertices
        self.triangles = triangles
        self.color = color
        self.n = int(len(self.triangles) / 3)
        self.normals = self.__calc_normals()
        self.centroids = self.__calc_centroids()


    def get_triangle(self, i):
        return self.triangles[3*i:3*i+3]


    def __calc_normals(self):
        n = int(len(self.triangles) / 3)
        normals = []
        for i in range(n):
            p1, p2, p3 = self.get_triangle(i)
            p1 = self.vertices[p1].vec[:3]
            p2 = self.vertices[p2].vec[:3]
            p3 = self.vertices[p3].vec[:3]
            N = np.cross(p2-p1, p3-p1)
            N = N / np.linalg.norm(N)
            normals.append(N)
        return normals


    def is_visible(self, id_, v:Vector3):
        u = self.centroids[id_]
        n = self.normals[id_]
        v = u - v
        x = (v.vec[:3]/np.linalg.norm(v.vec[:3])).dot(n/np.linalg.norm(n))
        return True if x > 0 else False


    def __calc_centroids(self):
        n = int(len(self.triangles) / 3)
        centroids = []
        for i in range(n):
            p1, p2, p3 = self.get_triangle(i)
            p1 = self.vertices[p1].vec[:3]
            p2 = self.vertices[p2].vec[:3]
            p3 = self.vertices[p3].vec[:3]
            x = (p1[0] + p2[0] + p3[0]) / 3
            y = (p1[1] + p2[1] + p3[1]) / 3
            z = (p1[2] + p2[2] + p3[2]) / 3
            centroids.append(Vector3(x, y, z))
        return centroids


    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < self.n:
            p1, p2, p3 = self.get_triangle(self.i)
            p1 = self.vertices[p1].vec[:3]
            p2 = self.vertices[p2].vec[:3]
            p3 = self.vertices[p3].vec[:3]
            color = self.color[self.i]
            n = self.normals[self.i]
            self.i += 1
            return (p1, p2, p3, n, color)
        raise StopIteration


if __name__ == '__main__':
    m = Mesh([Vector3(0,0,0), Vector3(1,2,3), Vector3(4,5,6)], [0,1,2, 0,2,1], ['red', 'red'])
    for i in m:
        print(i)




    