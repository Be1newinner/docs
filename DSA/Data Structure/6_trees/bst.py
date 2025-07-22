from __future__ import annotations

# 2. Binary Search Tree (BST) ==============================================================================
# What: A binary tree where left.val < node.val < right.val.
# Why: Enables O(log n) search/insert/delete (if balanced).

# Must‑know operations:
# insert, search, delete
# Validate BST
# Kth smallest/largest element
# Floor/ceil, range queries

# Practice:
# LeetCode 98: Validate BST
# LeetCode 230: Kth Smallest BST
# LeetCode 450: Delete Node in a BST

class BST:
    def __init__(self, data: int):
        self.data = data
        self.left: BST = None
        self.right: BST = None
        
    def insert(self, data: int): 
        if not data:
            return
        
        if self.data == data:
            return
        
        if data < self.data:
            if self.left:
                self.left.insert(data)
            else:
                self.left = BST(data)
            
        else:
            if self.right:
                self.right.insert(data)
            else:
                self.right = BST(data)
                
    def inorder(self:BST):
        def _inorder(node: BST):
            if node:
                _inorder(node.left)
                print(node.data)
                _inorder(node.right)
        return _inorder(self)
    
    def preorder(self: BST):
        def _preorder(node: BST):
            if not node:
                return
            print(node.data)
            _preorder(node.left)
            _preorder(node.right)
        return _preorder(self)
    
    def search(self: BST, data:int):
        def _search(node: BST, data: int):
            if not node:
                return False
            if data == node.data:
                return True
            elif data < node.data:
                return  _search(node.left, data)
            else:
                return _search(node.right, data)
        return _search(self, data)
    
    def delete(self: BST, data: int):
        pass
                    
bst = BST(21)
bst.insert(2)
bst.insert(4)
bst.insert(3)
bst.insert(5)
bst.insert(29)
bst.insert(11)
bst.insert(23)
bst.insert(5)
print("INSERT ENDS!")

bst.inorder()

# print(bst.search(23))