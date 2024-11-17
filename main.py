
class   Node:
    # fix the color shit
    def __init__(self, lft: "Node", val, color, rgt: "Node") -> None:
        self._lft = lft
        self._val = val
        self._color = color
        self._rgt = rgt


    @property
    def lft(self):
        return self._lft
    
    @lft.setter
    def lft(self, lft):
        raise ValueError("cannot set lft")
    
    @property
    def val(self):
        return self._val
    
    @val.setter
    def val(self, val):
        raise ValueError("cannot set val")
    
    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color):
        raise ValueError("cannot set color")
    
    @property
    def rgt(self):
        return self._rgt
    
    @rgt.setter
    def rgt(self, rgt):
        raise ValueError("cannot set rgt")
    
class Tree:
    def __init__(self, root: "Node") -> None:
        self._root = root

    @property
    def root(self):
        return self._root
    
    @root.setter
    def root(self, root):
        raise ValueError("cannot set root")

    
def treeFromTrees(lft: Tree, val, rgt: Tree) -> Tree:
    node = Node(lft.root, val, rgt.root)
    return Tree(node)

def printNode(node: Node):
    if node is None: 
        print("leaf / None")
    else:
        print(node.val, node.color)
        printNode(node.lft)
        printNode(node.rgt)


def printTree(tree: Tree):
    printNode(tree.root)
    print("*" * 80)

def insertNode(node: Node, val) -> Node:
    # new inserted node is always red
    if node is None:
        return Node(None, val, "red", None)
    elif node.val > val:
        return Node(insertNode(node.lft, val), node.val, node.color, node.rgt)
    elif node.val < val:
        return Node(node.lft, node.val, node.color, insertNode(node.rgt, val))
    else:
        # repeated values are discarded 
        pass

def insertNodeIntoTree(tree: Tree, val) -> Tree:
    return Tree(insertNode(tree.root, val))

def leftRotateNode(node: Node) -> Node:
    if node is None or node.rgt is None:
        return node
    lNode = Node(node.lft, node.val, node.color, node.rgt.lft)
    rNode = node.rgt.rgt
    return Node(lNode, node.rgt.val, node.rgt.color, rNode)

def rightRotateNode(node: Node) -> Node:
    if node is None or node.lft is None:
        return node
    lNode = node.lft.lft
    rNode = Node(node.lft.rgt, node.val, node.color, node.rgt)
    return Node(lNode, node.lft.val, node.lft.color, rNode)

def findNode(node: Node, val) -> Node:
    if node is None:
        return None
    if val < node.val:
        return findNode(node.lft, val)
    elif val > node.val:
        return findNode(node.rgt, val)
    else: 
        # same value
        return node
    
def findParentNode(node: Node, val) -> Node:
    if node is None:
        return None
    if val < node.val:
        if node.lft is not None and node.lft.val == val:
            return node
        else:
            return findParentNode(node.lft, val)
    elif val > node.val:
        if node.rgt is not None and node.rgt.val == val:
            return node
        else:
            return findParentNode(node.rgt, val)
    else:
        # same value
        return None
    
def redBlackInsertion(tree: Tree, val) -> Tree: 
    treeStep1 = insertNodeIntoTree(tree, val)
    # parent of new Node is black
    parentNode = findParentNode(tree.root, val)
    if parentNode.color == "black":
        return treeStep1
    # fixes required, find uncle node
    opaNode = findParentNode(tree.root, parentNode.val)
    if opaNode.val > parentNode.val:
        uncleNode = opaNode.rgt
    else:
        uncleNode = opaNode.lft



def testInsert():
    
    tree1 = Tree(None)
    printTree(tree1)
    tree2 = insertNodeIntoTree(tree1, 10)
    printTree(tree2)
    tree3 = insertNodeIntoTree(tree2, 5)
    printTree(tree3)
    tree4 = insertNodeIntoTree(tree3, 7)
    printTree(tree4)
    


def testLeftRotate():
    tree = Tree(None)
    tree = insertNodeIntoTree(tree, 5)
    tree = insertNodeIntoTree(tree, 10)
    tree = insertNodeIntoTree(tree, 7)
    tree = insertNodeIntoTree(tree, 12)
    printTree(tree)

    lRotated = leftRotateNode(tree.root)
    rotatedTree = Tree(lRotated)
    printTree(rotatedTree)

def testRightRotate():
    tree = Tree(None)
    tree = insertNodeIntoTree(tree, 10)
    tree = insertNodeIntoTree(tree, 5)
    tree = insertNodeIntoTree(tree, 3)
    tree = insertNodeIntoTree(tree, 7)
    printTree(tree)

    rRotated = rightRotateNode(tree.root)
    rotatedTree = Tree(rRotated)
    printTree(rotatedTree)
    

def main():
   # testLeftRotate()
    testRightRotate()


if __name__ == "__main__":
    main()
