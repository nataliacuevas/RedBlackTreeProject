from collections import namedtuple

# Define the Red-Black Tree Node as an immutable namedtuple
Node = namedtuple("Node", ["value", "color", "left", "right"])
Leaf = Node(value=None, color="black", left=None, right=None) 

class RBTree:
    def __init__(self, root: Node):
        self.root = root

    
def printNode(node: Node) -> None:
    if node == Leaf: 
        print("Leaf")
    else:
        print(node.value, node.color)
        printNode(node.left)
        printNode(node.right)


def printTree(tree: RBTree) -> None:
    printNode(tree.root)
    print("*" * 80)

def insertNode(node: Node, value, color="red") -> Node:
    # new inserted node is always red
    if node == Leaf:
        return  Node(value=value, color=color, left=Leaf, right=Leaf)
    elif node.value > value:
        return Node(value=node.value, color=node.color, left=insertNode(node.left, value, color=color), right=node.right)
    elif node.value < value:
        return Node(value=node.value, color=node.color, left=node.left, right=insertNode(node.right, value, color=color))
    else:
        # repeated values are discarded
        return node


def insertNodeIntoTree(tree: RBTree, value, color="red") -> RBTree:
    return RBTree(insertNode(tree.root, value, color))

def leftRotateNode(node: Node) -> Node:
    if node == Leaf or node.right == Leaf:
        return node
    lNode = Node(value=node.value, color=node.color, left=node.left, right=node.right.left)
    rNode = node.right.right
    return Node(value=node.right.value, color=node.right.color, left=lNode, right=rNode)

def rightRotateNode(node: Node) -> Node:
    if node == Leaf or node.left == Leaf:
        return node
    lNode = node.left.left
    rNode = Node(value=node.value, color=node.color, left=node.left.right, right=node.right)
    return Node(value=node.left.value, color=node.left.color, left=lNode, right=rNode)

def findNode(node: Node, value) -> Node:
    if node == Leaf:
        return Leaf
    if value < node.value:
        return findNode(node.left, value)
    elif value > node.value:
        return findNode(node.right, value)
    else: 
        # same value
        return node


def findParentNode(node: Node, value) -> Node:
    if node == Leaf:
        return Leaf
    if value < node.value:
        if node.left != Leaf and node.left.value == value:
            return node
        else:
            return findParentNode(node.left, value)
    elif value > node.value:
        if node.right != Leaf and node.right.value == value:
            return node
        else:
            return findParentNode(node.right, value)
    else:
        # same value, this is like None
        return Leaf
    
    
def findOpaNode(node: Node, value) -> Node:
    parent = findParentNode(node, value)
    if parent == Leaf:
        return Leaf
    return  findParentNode(node, parent.value)

def findSiblingNode(node: Node, value) -> Node: 
    parentNode = findParentNode(node, value)
    if parentNode == Leaf: 
        return Leaf
    if value < parentNode.value:
        return parentNode.right
    else:
        return parentNode.left

""" 
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

"""
# https://www.geeksforgeeks.org/red-black-tree-in-python/


def compareNodes(node1: Node, node2: Node) -> bool:
    if node1 == Leaf and node2 == Leaf: 
        return True

    # If one of the nodes is Leaf or their values/colors don't match
    if node1 == Leaf or node2 == Leaf or node1 != node2:
        return False

    # Recursively compare left and right subtrees
    return (compareNodes(node1.left, node2.left) and
            compareNodes(node1.right, node2.right))

def compare2Trees(tree1: RBTree, tree2: RBTree) -> bool:
    return compareNodes(tree1.root, tree2.root)

def case1(node: Node, value) -> bool:
    parent = findParentNode(node, value) 
    uncle = findSiblingNode(node, parent.value)

    if parent.color == "red" and uncle.color == "red":
        return True
    else:
        return False

def fixCase1(node: Node, opaValue) ->  Node:
    if node.value == opaValue:
        newLeftChild = node.left._replace(color="black")
        newRightChild = node.right._replace(color="black")
        return Node(value=node.value, color="red", left=newLeftChild, right=newRightChild)
    
    if node.value < opaValue: 
        return Node(value=node.value, color=node.color, left=node.left, right=fixCase1(node.right, opaValue))
      #  return node._replace(right=fixCase1(node.right, opaValue))

    else: 
        return Node(value=node.value, color=node.color, left=fixCase1(node.left, opaValue), right=node.right)
      #  return node._replace(left=fixCase1(node.left, opaValue))

def FullFixCase1(root: Node, value) -> Node:
   #  if case1(node, value): 
    opa = findOpaNode(root, value)

    if opa == Leaf:
        return root # no grandpa case 
    if opa.left.color == "red" and opa.right.color == "red":
        newNode = fixCase1(root, opa.value)
        newRoot = FullFixCase1(newNode, opa.value)
        return newRoot._replace(color="black")
    else: # not case 1 
        return root
    
#    Case 2: Rotation and Recoloring
# If the new node’s uncle is black and the new node is the right child of a left child (or vice versa),
#  perform a rotation to move the new node up and align it.

# If the new node’s uncle is black and the new node is the left child of a left child (or right of a right), 
# perform a rotation and recolor the parent and grandparent to fix the violation.

def fixCase2(root: Node, value) -> Node:
    parentNode = findParentNode(root, value)
    opaNode = findOpaNode(root, value)
    

    uncleNode = opaNode.
    if paren

    return root

def testFullFixCase1():
    print("testing full fix case 1")
    tree = RBTree(Node(value=50, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 40)
    tree = insertNodeIntoTree(tree, 70)
    tree = insertNodeIntoTree(tree, 80, color="black")
    tree = insertNodeIntoTree(tree, 75)
    tree = insertNodeIntoTree(tree, 90)
    tree = insertNodeIntoTree(tree, 100)

    fixedRoot = FullFixCase1(tree.root, 100)
    expectedTree = RBTree(Node(value=50, color="black", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 40, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 70, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 80, color="red")
    expectedTree = insertNodeIntoTree(expectedTree, 75, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 90, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 100)

    unexpectedTree = RBTree(Node(value=50, color="black", left=Leaf, right=Leaf))
    unexpectedTree = insertNodeIntoTree(unexpectedTree, 40, color="black")
    unexpectedTree = insertNodeIntoTree(unexpectedTree, 70, color="black")
    unexpectedTree = insertNodeIntoTree(unexpectedTree, 80, color="black")
    unexpectedTree = insertNodeIntoTree(unexpectedTree, 75, color="black")
    unexpectedTree = insertNodeIntoTree(unexpectedTree, 90, color="black")
    unexpectedTree = insertNodeIntoTree(unexpectedTree, 100)
    assert(not compareNodes(fixedRoot, unexpectedTree.root))


    



def testFindOpaNode(): 
    print("testing opa node")
    tree = RBTree(Node(value=10, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 6)
    tree = insertNodeIntoTree(tree, 8)
    opa = findOpaNode(tree.root, 8)
    parent = findParentNode(tree.root, 8)
    
    assert(opa == tree.root)
    assert(opa != parent)
    assert(parent == opa.left)


def testCompare2Trees():

    print("testing compare2Trees")
    tree1 = RBTree(Node(value=10, color="black", left=Leaf, right=Leaf))
    tree3 = insertNodeIntoTree(tree1, 5)
    tree4 = insertNodeIntoTree(tree3, 7)

    tree5 = RBTree(Node(value=10, color="black", left=Leaf, right=Leaf))
    tree7 = insertNodeIntoTree(tree5, 5)
    tree8 = insertNodeIntoTree(tree7, 7)

    tree9 = RBTree(Node(value=10, color="black", left=Leaf, right=Leaf))
    tree11 = insertNodeIntoTree(tree9, 4)
    tree12 = insertNodeIntoTree(tree11, 7)

    assert(compare2Trees(tree4, tree8))
    assert(not compare2Trees(tree8, tree12))


def testInsert():
    
    print("testing insert")
    tree1 = RBTree(Node(value=10, color="black", left=Leaf, right=Leaf))
    tree2 = insertNodeIntoTree(tree1, 5)
    tree3 = insertNodeIntoTree(tree2, 7)

    tree4 = RBTree(Node(value=10, color="black", left=Leaf, right=Leaf))
    tree5 = insertNodeIntoTree(tree4, 5)
    tree6 = insertNodeIntoTree(tree5, 7)
    tree7 = insertNodeIntoTree(tree6, 5)

    assert(compare2Trees(tree7, tree3))
       

def testLeftRotate():
    print("testing left rotation")
    tree = RBTree(Node(value= 5, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 10, color="red")
    tree = insertNodeIntoTree(tree, 7, color="red")
    tree = insertNodeIntoTree(tree, 12, color="red")

    lRotated = leftRotateNode(tree.root)
    expectedTree =RBTree(Node(value=10, color="red", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 5, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 12, color="red")
    expectedTree = insertNodeIntoTree(expectedTree, 7, color="red")
                    
    assert(compareNodes(lRotated, expectedTree.root))


def testRightRotate():

    print("testing right rotation")
    tree = RBTree(Node(value= 15, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 10, color="red")
    tree = insertNodeIntoTree(tree, 7, color="red")
    tree = insertNodeIntoTree(tree, 12, color="red")

    rRotated = rightRotateNode(tree.root)
    expectedTree =RBTree(Node(value=10, color="red", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 15, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 12, color="red")
    expectedTree = insertNodeIntoTree(expectedTree, 7, color="red")
                
    assert(compareNodes(rRotated, expectedTree.root))


def main():

    testInsert()
    testCompare2Trees()
    testFindOpaNode()
    testLeftRotate()
    testRightRotate()
    testFullFixCase1()


if __name__ == "__main__":
    main()
