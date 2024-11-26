from collections import namedtuple
import re
import sys

# Define the Red-Black Tree Node as an immutable namedtuple
Node = namedtuple("Node", ["value", "color", "left", "right"])
Leaf = Node(value=None, color="black", left=None, right=None) 

# TODO: make RBTree a named tuple
class RBTree:
    def __init__(self, root: Node):
        self.root = root

def insertNode(node: Node, value, color="red") -> Node:
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

def compareNodes(node1: Node, node2: Node) -> bool:
    if node1 == Leaf and node2 == Leaf: 
        return True
    if node1.value != node2.value or node1.color != node2.color:
        return False
    # Recursively compare left and right subtrees
    return (compareNodes(node1.left, node2.left) and
            compareNodes(node1.right, node2.right))

def compare2Trees(tree1: RBTree, tree2: RBTree) -> bool:
    return compareNodes(tree1.root, tree2.root)

# Reference: https://www.formosa1544.com/2021/04/30/build-the-forest-in-python-series-red-black-tree/#2-build-red-black-tree

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

def handleInput() -> str:
    if len(sys.argv) != 2:
        raise ValueError("The script requires a filename to read from, please input it")
    return sys.argv[1]

def main():
    filename = handleInput()

    print("Reading file and tokenizing")
    text = process_file(filename)
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
