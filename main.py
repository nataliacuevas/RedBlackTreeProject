from collections import namedtuple
import re

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
    if node1 == Leaf or node2 == Leaf or node1.value != node2.value or node1.color != node2.color:
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
    # this fn assumes there is a case 1 to fix

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
    

def isRightChild(root: Node, value) -> bool:
    parent = findParentNode(root, value)
    if parent == Leaf: 
        return False 
    if value > parent.value:
        return True
    else: 
        return False
    
def case2(node: Node, value) -> bool:
    parent = findParentNode(node, value) 
    uncle = findSiblingNode(node, parent.value)
    if uncle.color == "black":
        return True
    else:
        return False

def fixCase2Old(root: Node, value) -> Node:

    opa = findOpaNode(root, value)
    parent = findParentNode(root, value)
    uncle = findSiblingNode(root, parent.value)

    if opa == Leaf:
        return root # no grandpa case 
    # uncle is black and node is right-child 
    if (isRightChild(root, value)) and uncle.color == "black":
        lRotatedParent = leftRotateNode(parent)
        return lRotatedParent
    # uncle is black and node is left-child 
    elif(isRightChild(root, value) != True) and uncle.color == "black":
        rRotatedOpa = rightRotateNode(opa)
        return rRotatedOpa
    else: # not case 2
        return root 
    # Todo: recolor appropiately 

def fixCase2(node: Node, value, opaValue) -> Node:
    # this fn assumes there is a case 2 to fix
    if node.value < opaValue:
        return node._replace(right= fixCase2(node.right, value, opaValue))
    elif node.value > opaValue:
        return node._replace(left= fixCase2(node.left, value, opaValue))
    else: # node is the opavalue
        if value < opaValue and value < node.left.value:
            rRotated = rightRotateNode(node)

# Case 1&4: Sibling of parent red
def fixCase_SR(opaNode: Node) -> Node:
    recolorLeft = opaNode.left._replace(color="black")
    recolorRight = opaNode.right._replace(color="black")
    return opaNode._replace(left=recolorLeft, right=recolorRight, color="red")

# Case 2: Parent is left Child, Sibling of parent black, Inserted node right child
def fixCase_PL_SB_IR(opaNode: Node) -> Node:
    # transfer case 2 to case 3
    intermediateOpa = opaNode._replace(left=leftRotateNode(opaNode.left))
    return fixCase_PL_SB_IL(intermediateOpa)

# Case 3: Parent is left Child, Sibling of parent black, Inserted node left child
def fixCase_PL_SB_IL(opaNode: Node) -> Node:
    recolorParent = opaNode.left._replace(color="black")
    newOpa = opaNode._replace(color="red", left=recolorParent)
    return rightRotateNode(newOpa)

# Case 5: Parent is right Child, Sibling of parent black, Inserted node left child
def fixCase_PR_SB_IL(opaNode: Node) -> Node:
    # transfer case 5 to 6
    intermediateOpa = opaNode._replace(right=rightRotateNode(opaNode.right))
    return fixCase_PR_SB_IR(intermediateOpa)

# Case 6: Parent is right Child, Sibling of parent black, Inserted node right child
def fixCase_PR_SB_IR(opaNode: Node) -> Node:
    recolorParent = opaNode.right._replace(color="black")
    recolorOpa = opaNode._replace(color="red", right=recolorParent)
    return leftRotateNode(recolorOpa)


# Assess the node and returns the grandparent node and the case
def assessNode(root: Node, fixValue) -> str:
    parentNode = findParentNode(root, fixValue)
    if fixValue == root.value and root.color == "red":
        return "RedRoot"
    if parentNode.color == "red":
        opaNode = findParentNode(root, parentNode.value)
        siblingNode = findSiblingNode(root, parentNode.value)
        if siblingNode.color == "red":
            return "fixCase_SR"
        else:
            if parentNode.value < opaNode.value:
                if parentNode.value < fixValue:
                    return "fixCase_PL_SB_IR"
                else:
                    return "fixCase_PL_SB_IL"
            else:
                if parentNode.value < fixValue:
                    return "fixCase_PR_SB_IR"
                else:
                    return "fixCase_PR_SB_IL"
    return "NothingToFix"

def applyInsertionFix(node: Node, opaNode: Node, fixFunction) -> Node:
    if opaNode.value < node.value:
        return node._replace(left=applyInsertionFix(node.left, opaNode, fixFunction))
    elif opaNode.value > node.value:
        return node._replace(right=applyInsertionFix(node.right, opaNode, fixFunction))
    else: # We are at the grandparent!
        return fixFunction(opaNode)

# To help us map between cases and functions
fixDictionary = {"fixCase_SR": fixCase_SR,
                 "fixCase_PL_SB_IR": fixCase_PL_SB_IR,
                 "fixCase_PL_SB_IL": fixCase_PL_SB_IL,
                 "fixCase_PR_SB_IR": fixCase_PR_SB_IR,
                 "fixCase_PR_SB_IL": fixCase_PR_SB_IL
                 }

def fixInsertion(root: Node, fixValue) -> Node:
    assessment = assessNode(root, fixValue)
    if assessment == "RedRoot":
        return root._replace(color="black")
    elif assessment == "NothingToFix":
        return root
    opaNode = findOpaNode(root,  fixValue)
    fixFunction = fixDictionary[assessment]
    newRoot = applyInsertionFix(root, opaNode, fixFunction)
    # repeat the process on the grandpa node
    return fixInsertion(newRoot, opaNode.value)

def insertNodeIntoRBTree(tree: RBTree, value) -> RBTree:
    insertionRoot = insertNode(tree.root, value)
    return RBTree(fixInsertion(insertionRoot, value))

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

def tokenize(text):
    #Tokenize text into words, removing punctuation and converting to lowercase
    return re.findall(r'\b[a-zA-Z]+\b', text.lower())

def process_file(file_path):
    #Read the file and return its content
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def inOrderTraversal(node: Node) -> list[str]:
    if node == Leaf:
        return []
    return inOrderTraversal(node.left) + [node.value] + inOrderTraversal(node.right)

def writeOutput(file_path, sorted_words):
    #Write the sorted words to the output file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("\n".join(sorted_words))

def main():
    print("Reading file and tokenizing")
    text = process_file("war_and_peace.txt")
    words = tokenize(text)

    print("Inserting words into Red Black Tree")
    tree = RBTree(Leaf)
    for word in words:
        tree = insertNodeIntoRBTree(tree, word)

    print("Getting sorted list of words")
    sortedWords = inOrderTraversal(tree.root)

    print("Writing output to output.txt file")
    writeOutput("output.txt", sortedWords)


if __name__ == "__main__":
    main()
