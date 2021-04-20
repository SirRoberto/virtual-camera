from Triangle import Triangle
from BST import BST, Node
from vector import Vector3
import numpy as np

class BinarySpacePartitioning():
    def __init__(self, objects:list):
        self.objects = objects.copy()
        self.n = self.n_polygons()
        self.new_polygons = []
        self.bst = self.generate_bst([i for i in range(self.n)])


    def getOrderedPolygons(self, pos:Vector3):
        root = self.bst.root
        order = self.traversal(root, pos)
        polygons = []
        for i in order:
            polygons.append(self.get_polygon(i))
        return polygons


    def traversal(self, parent:Node, pos:Vector3):
        order = []
        if parent.isLeaf():
            if parent.value:
                order += parent.value
        elif self.determine_observator_location(parent.value[0], pos) == 1:
            if parent.rightNode:
                order += self.traversal(parent.rightNode, pos)
            if parent.value:
                order += parent.value
            if parent.leftNode:
                order += self.traversal(parent.leftNode, pos)
        elif self.determine_observator_location(parent.value[0], pos) == -1:
            if parent.leftNode:
                order += self.traversal(parent.leftNode, pos)
            if parent.value:
                order += parent.value
            if parent.rightNode:
                order += self.traversal(parent.rightNode, pos)
        elif self.determine_observator_location(parent.value[0], pos) == 0:
            if parent.leftNode:
                order += self.traversal(parent.leftNode, pos)
            if parent.rightNode:
                order += self.traversal(parent.rightNode, pos)
        return order


    def generate_bst(self, polygons, x=0):
        bst = BST(Node(polygons))
        parent = bst.root
        self.build_tree(parent, x)
        return bst


    def build_tree(self, parent:Node, x=0):
        fronts, behinds, toDivides = self.determine_location(parent.value[x], parent.value[0:x] + parent.value[x+1:])
        if len(toDivides) > 0:
            new_polygons = self.divide_polygons(parent.value[x], toDivides)
            if new_polygons:
                fronts_, behinds_, containingX = self.determine_location(parent.value[x], new_polygons)
                fronts += fronts_
                behinds += behinds_
                parent.value = [parent.value[x]]
                parent.value += containingX

        if len(fronts) > 0:
            parent.addLeftNode(fronts)
            self.build_tree(parent.leftNode)
        if len(behinds) > 0:
            parent.addRigthNode(behinds)
            self.build_tree(parent.rightNode)


    def determine_location(self, x, polygons):
        surface = self.get_polygon(x)
        n_s = surface[-2]
        behinds = []
        fronts = []
        toDivides = []
        for polygon_id in polygons:
            polygon = self.get_polygon(polygon_id)
            is_behind = []
            is_front = []

            for point in polygon[:-2]:
                v = point - surface[0]
                dot = v.dot(n_s)
                if abs(dot) < 1e-6:
                    dot = 0

                if dot < 0.0:
                    is_behind.append(True)
                    is_front.append(False)
                elif dot > 0.0:
                    is_behind.append(False)
                    is_front.append(True)

            if any(is_behind) == any(is_front):
                toDivides.append(polygon_id)
            elif any(is_front):
                fronts.append(polygon_id)
            else:
                behinds.append(polygon_id)
        
        return fronts, behinds, toDivides


    def determine_observator_location(self, polygon_id, pos: Vector3):
        surface = self.get_polygon(polygon_id)
        n_s = surface[-2]
        v = pos.vec[:3] - surface[0]
        dot = v.dot(n_s)
        if dot < 0.0:
            return -1
        elif dot > 0.0:
            return 1
        else:
            return 0


    def divide_polygons(self, x, polygons, eps=1e-16):
        surface = self.get_polygon(x)
        n_s = surface[-2]
        p_s = surface[0]
        n = self.n

        for i, polygon_id in enumerate(polygons):
            polygon = self.get_polygon(polygon_id)
            new_points = self.isect_polygon_plane(n_s, p_s, polygon_id)
            if all(v is None for v in new_points):
                self.new_polygons.append(polygon)
                self.n += 1
                continue

            new_polygon_1 = []
            new_polygon_2 = []
            iter_point = iter(polygon[:-2])
            iter_new_point = iter(new_points)
            sentry = False
            while True:
                try:
                    point = next(iter_point)
                    if not sentry:
                        new_polygon_1.append(point)
                    else:
                        new_polygon_2.append(point)

                    new_point = next(iter_new_point)
                    if new_point is not None:
                        sentry = not sentry
                        new_polygon_1.append(new_point)
                        new_polygon_2.append(new_point)
                except StopIteration:
                    break

            new_polygon_1 += polygon[-2:]
            new_polygon_2 += polygon[-2:]

            self.new_polygons.append(new_polygon_1)
            self.new_polygons.append(new_polygon_2)
            self.n += 2

        return [i for i in range(n, self.n)]

    
    def isect_polygon_plane(self, n_s, p_s, polygon_id, eps=1e-16):
        polygon = self.get_polygon(polygon_id)
        new_points = []
        for i, p0 in enumerate(polygon[:-2]):
            if i+1 < len(polygon[:-2]):
                p1 = polygon[i+1]
            else:
                p1 = polygon[0]

            point = self.isect_section_plane(p0, p1, n_s, p_s)

            if point is None:
                new_points.append(None)
            else:
                same = False
                for p in new_points:
                    if p is None:
                        continue
                    dist = np.linalg.norm(point - p)
                    if dist < eps:
                        same = True
                        break
                if not same:
                    new_points.append(point)
                else:
                    new_points.append(None)
                
        return new_points


    def isect_section_plane(self, p0, p1, n_s, p_s, eps=1e-6):
        point = self.isect_line_plane(p0, p1, n_s, p_s, eps)
        if point is None:
            return None
        min_X, max_X = min(p0[0], p1[0]) - eps, max(p0[0], p1[0]) + eps
        min_Y, max_Y = min(p0[1], p1[1]) - eps, max(p0[1], p1[1]) + eps
        min_Z, max_Z = min(p0[2], p1[2]) - eps, max(p0[2], p1[2]) + eps
        if ((min_X <= point[0]) and (point[0] <= max_X) and 
            (min_Y <= point[1]) and (point[1] <= max_Y) and
            (min_Z <= point[2]) and (point[2] <= max_Z)):
            return point
        return None



    def isect_line_plane(self, p0, p1, n_s, p_s, eps=1e-6):
        if np.linalg.norm(p1 - p0) > eps:
            u = (p1 - p0) / np.linalg.norm(p1 - p0)
            if abs(n_s.dot(u)) < eps:
                return None
            t = n_s.dot(p_s - p0) / n_s.dot(u)
            return p0 + t * u
        else:
            p = (p1 + p0) / 2
            if self.does_plain_contain_point(p, n_s, p_s):
                return p
            else:
                return None


    def does_plain_contain_point(self, point, n_s, p_s, eps=1e-6):
        return abs(n_s.dot(point - p_s)) < eps


    def n_polygons(self):
        n = 0
        for o in self.objects:
            n += o.mesh.n
        return n


    def get_polygon(self, i):
        j = 0
        for o in self.objects:
            for m in o.mesh:
                if i == j:
                    return m
                j += 1
        return self.new_polygons[i-j]

if __name__ == '__main__':
    p = BinarySpacePartitioning([
        Triangle(Vector3(0,0,0), Vector3(1,1,1), Vector3())
    ])