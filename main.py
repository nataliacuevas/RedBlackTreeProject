
class   Node:
    def __init__(self, lft: "Node", val, rgt: "Node") -> None:
        self._lft = lft
        self._val = val
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
        print(node.val)
        printNode(node.lft)
        printNode(node.rgt)


def printTree(tree: Tree):
    printNode(tree.root)



def main():
    n = Node(None, 1, None)
 
    node2 = Node(None, 2, None)
    tree1 = Tree(n)
    tree2 = Tree(node2)
    tree3 = treeFromTrees(tree1, 3, tree2)
    printTree(tree3)

if __name__ == "__main__":
    main()
