from vector import Vector3, Vector2

class Node():
    def __init__(self, value, leftNode=None, rightNode=None):
        self.value = value
        self.leftNode = leftNode
        self.rightNode = rightNode

    def addLeftNode(self, value, left=None, right=None):
        self.leftNode = Node(value, Node(left), Node(right))

    def addRigthNode(self, value, left=None, right=None):
        self.rightNode = Node(value, Node(left), Node(right))

    def isLeaf(self):
        return (self.leftNode is None) and (self.rightNode is None)

class BST():
    def __init__(self, root:Node=None):
        self.root = root

    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.leftNode) 
            res.append(root.value)
            res = res + self.inorderTraversal(root.rightNode)
        return res

    def levelOrderTraversal(self, root):
        thislevel = [root]
        visited = []
        while thislevel:
            nextlevel = []
            for n in thislevel:
                visited.append(n.value)
                if n.leftNode:
                    nextlevel.append(n.leftNode)
                if n.rightNode:
                    nextlevel.append(n.rightNode)
            thislevel = nextlevel
        return visited



if __name__ == '__main__':
    bst = BST(Node([10,20]))
    bst.root.addLeftNode([10])
    print(bst.root.value, bst.root.rigthNode)