from collections import deque

# 1. Binary Tree ======================================================================================================
# What: Each node has up to two children (left, right).
# Why: Foundation for all tree algorithms.
# Must‑know operations & patterns:

# Traversals: preorder, inorder, postorder, level‑order
# Height / Max depth, Diameter of tree
# Path‑sum problems (root→leaf sums)
# Invert/reconstruct (mirror)
# Lowest Common Ancestor (LCA)

# Practice:
# LeetCode 100: Same Tree
# LeetCode 104: Maximum Depth
# LeetCode 226: Invert Binary Tree
# LeetCode 236: LCA of Binary Tree

class TreeNode:
    def __init__(self, value):
        self.val = value
        self.left = None
        self.right = None

def build_binary_tree_from_list(arr):
    if not arr or not len(arr):
        return None
    
    root = TreeNode(arr[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(arr):
        current = queue.popleft()

        # Left Child
        if i < len(arr) and arr[i] is not None:
            current.left = TreeNode(arr[i])
            queue.append(current.left)
        i += 1

        # Right Child
        if i < len(arr) and arr[i] is not None:
            current.right = TreeNode(arr[i])
            queue.append(current.right)
        i += 1

    return root

arr = [1, 2, 3, None, 4, None, 5]
root = build_binary_tree_from_list(arr)

def inorder(root):
    if not root: return
    inorder(root.left)
    print(root.val, end=' ')
    inorder(root.right)

# inorder(root)  

# bst = BST()
# bst.insert(2)
# bst.insert(4)
# bst.insert(15)
# bst.insert(29)
# bst.insert(11)
# bst.insert(23)
# bst.insert(5)

# bst.inorder()

# bst.preorder()

# print(bst.search(23))