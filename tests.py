from main import *



def test_FindOpaNode(): 
    print("testing opa node")
    # Arrange
    tree = RBTree(Node(value=10, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 6)
    tree = insertNodeIntoTree(tree, 8)
    # Act
    opa = findOpaNode(tree.root, 8)
    parent = findParentNode(tree.root, 8)
    # Assert
    assert(opa == tree.root)
    assert(opa != parent)
    assert(parent == opa.left)


def test_Compare2Trees():
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


def test_Insert():
    
    print("testing insert")
    tree1 = RBTree(Node(value=10, color="black", left=Leaf, right=Leaf))
    tree2 = insertNodeIntoTree(tree1, 5)
    tree3 = insertNodeIntoTree(tree2, 7)

    tree4 = RBTree(Node(value=10, color="black", left=Leaf, right=Leaf))
    tree5 = insertNodeIntoTree(tree4, 5)
    tree6 = insertNodeIntoTree(tree5, 7)
    tree7 = insertNodeIntoTree(tree6, 5)

    assert(compare2Trees(tree7, tree3))
       

def test_LeftRotate():
    print("testing left rotation")
    # Arrange
    tree = RBTree(Node(value= 5, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 10, color="red")
    tree = insertNodeIntoTree(tree, 7, color="red")
    tree = insertNodeIntoTree(tree, 12, color="red")
    # Act
    lRotated = leftRotateNode(tree.root)
    # Assert
    expectedTree =RBTree(Node(value=10, color="red", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 5, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 12, color="red")
    expectedTree = insertNodeIntoTree(expectedTree, 7, color="red")
                    
    assert(compareNodes(lRotated, expectedTree.root))


def test_RightRotate():

    print("testing right rotation")
    # Arrange
    tree = RBTree(Node(value= 15, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 10, color="red")
    tree = insertNodeIntoTree(tree, 7, color="red")
    tree = insertNodeIntoTree(tree, 12, color="red")
    # Act
    rRotated = rightRotateNode(tree.root)
    # Assert
    expectedTree =RBTree(Node(value=10, color="red", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 15, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 12, color="red")
    expectedTree = insertNodeIntoTree(expectedTree, 7, color="red")
                
    assert(compareNodes(rRotated, expectedTree.root))

def test_fixCaseSR_correct():
    print("testing fixCase_SR")
    # Arrange
    tree = RBTree(Node(value=23, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 11)
    tree = insertNodeIntoTree(tree, 37)
    insertedValue = 7
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    node = tree.root
    fixedNode = fixCase_SR(node)

    # Assert
    expectedTree = RBTree(Node(value=23, color="red", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 11, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 37, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, insertedValue, color="red")
    assert(compareNodes(expectedTree.root, fixedNode))

def test_fixCasePLSBIR_correct():
    print("testing fixCase_PL_SB_IR")
    #Arrange
    tree = RBTree(Node(value=11, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 7)
    insertedValue = 8
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    node = tree.root
    fixedNode = fixCase_PL_SB_IR(node)

    # Assert
    expectedTree = RBTree(Node(value=insertedValue, color="black", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 11, color="red")
    expectedTree = insertNodeIntoTree(expectedTree, 7, color="red")
    
    assert(compareNodes(expectedTree.root, fixedNode))

def test_fixCasePLSBIL_correct():
    print("testing fixCase_PL_SB_IL")
    #Arrange
    tree = RBTree(Node(value=11, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 8)
    insertedValue = 7
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    node = tree.root
    fixedNode = fixCase_PL_SB_IL(node)

    # Assert
    expectedTree = RBTree(Node(value=8, color="black", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 11, color="red")
    expectedTree = insertNodeIntoTree(expectedTree, insertedValue, color="red")
    
    assert(compareNodes(expectedTree.root, fixedNode))

def test_fixCasePRSBIL_correct():
    print("testing fixCase_PR_SB_IL")
    #Arrange
    tree = RBTree(Node(value=37, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 41)
    insertedValue = 39
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    node = tree.root
    fixedNode = fixCase_PR_SB_IL(node)

    # Assert
    expectedTree = RBTree(Node(value=insertedValue, color="black", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 37, color="red")
    expectedTree = insertNodeIntoTree(expectedTree, 41, color="red")
    
    assert(compareNodes(expectedTree.root, fixedNode))

def test_fixCasePRSBIR_correct():
    print("testing fixCase_PR_SB_IR")
    #Arrange
    tree = RBTree(Node(value=37, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 39)
    insertedValue = 41
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    node = tree.root
    fixedNode = fixCase_PR_SB_IR(node)

    # Assert
    expectedTree = RBTree(Node(value=39, color="black", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 37, color="red")
    expectedTree = insertNodeIntoTree(expectedTree, insertedValue, color="red")
    
    assert(compareNodes(expectedTree.root, fixedNode))

def test_assessNode_SR():
    print("testing assessNode with SR outcome")
    # Arrange
    tree = RBTree(Node(value=23, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 11)
    tree = insertNodeIntoTree(tree, 37)
    insertedValue = 7
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    assessment = assessNode(tree.root, insertedValue)
    # Assert
    assert(assessment == "fixCase_SR")


def test_assessNode_PLSBIR():
    print("testing assessNode with PL_SB_IR outcome")
    #Arrange
    tree = RBTree(Node(value=11, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 7)
    insertedValue = 8
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    assessment = assessNode(tree.root, insertedValue)
    # Assert
    assert(assessment == "fixCase_PL_SB_IR")

def test_assessNode_PLSBIL():
    print("testing assessNode with PL_SB_IL outcome")
    #Arrange
    tree = RBTree(Node(value=11, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 8)
    insertedValue = 7
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    assessment = assessNode(tree.root, insertedValue)
    # Assert
    assert(assessment == "fixCase_PL_SB_IL")

def test_assessNode_PRSBIR():
    print("testing assessNode with PR_SB_IR outcome")
    #Arrange
    tree = RBTree(Node(value=37, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 39)
    insertedValue = 41
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    assessment = assessNode(tree.root, insertedValue)
    # Assert
    assert(assessment == "fixCase_PR_SB_IR")

def test_assessNode_PRSBIL():
    print("testing assessNode with PR_SB_IL outcome")
    #Arrange
    tree = RBTree(Node(value=37, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 41)
    insertedValue = 39
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    assessment = assessNode(tree.root, insertedValue)
    # Assert
    assert(assessment == "fixCase_PR_SB_IL")
    
def test_assessNode_NothingToFix():
    print("testing assessNode with NothingToFix outcome")
    #Arrange
    tree = RBTree(Node(value=37, color="black", left=Leaf, right=Leaf))
    tree = insertNodeIntoTree(tree, 41, color="black")
    insertedValue = 44
    tree = insertNodeIntoTree(tree, insertedValue)

    # Act
    assessment = assessNode(tree.root, insertedValue)
    # Assert
    assert(assessment == "NothingToFix")

def test_assessNode_RedRoot():
    print("testing assessNode with RedRoot outcome")
    #Arrange
    tree = RBTree(Node(value=37, color="red", left=Leaf, right=Leaf))

    # Act
    assessment = assessNode(tree.root, 37)
    # Assert
    assert(assessment == "RedRoot")

def test_insertNodeIntoRBTree_3Insertions():
    print("testing insertNodeIntoRBTree 3 insertions")
    # Arrange
    tree = RBTree(Node(value=23, color="black", left=Leaf, right=Leaf))
    # Act
    tree = insertNodeIntoRBTree(tree, 11)
    tree = insertNodeIntoRBTree(tree, 37)
    tree = insertNodeIntoRBTree(tree, 7)

    # Assert
    expectedTree = RBTree(Node(value=23, color="black", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 37, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 11, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 7, color="red")
    assert(compare2Trees(tree, expectedTree))

def test_insertNodeIntoRBTree_4Insertions():
    print("testing insertNodeIntoRBTree 4 insertions")
    # Arrange
    tree = RBTree(Node(value=23, color="black", left=Leaf, right=Leaf))
    # Act
    tree = insertNodeIntoRBTree(tree, 11)
    tree = insertNodeIntoRBTree(tree, 37)
    tree = insertNodeIntoRBTree(tree, 7)
    tree = insertNodeIntoRBTree(tree, 9)

    # Assert
    expectedTree = RBTree(Node(value=23, color="black", left=Leaf, right=Leaf))
    expectedTree = insertNodeIntoTree(expectedTree, 37, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 9, color="black")
    expectedTree = insertNodeIntoTree(expectedTree, 7, color="red")
    expectedTree = insertNodeIntoTree(expectedTree, 11, color="red")
    assert(compare2Trees(tree, expectedTree))

if __name__ == "__main__":
    test_Insert()
    test_Compare2Trees()
    test_FindOpaNode()
    test_LeftRotate()
    test_RightRotate()
    test_fixCaseSR_correct()
    test_fixCasePLSBIR_correct()
    test_fixCasePLSBIL_correct()
    test_fixCasePRSBIL_correct()
    test_fixCasePRSBIR_correct()
    test_assessNode_SR()
    test_assessNode_PLSBIR()
    test_assessNode_PLSBIL()
    test_assessNode_PRSBIR()
    test_assessNode_PRSBIL()
    test_assessNode_NothingToFix()
    test_assessNode_RedRoot()
    test_insertNodeIntoRBTree_3Insertions()
    test_insertNodeIntoRBTree_4Insertions()