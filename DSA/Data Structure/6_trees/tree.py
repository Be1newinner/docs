'''
🌳 Types of Trees You Must Know for FAANG Interviews

1. Binary Tree (BT)	        
    a. Each node has ≤ 2 children	                            
    b. Foundation for all tree structures
2. Full Binary Tree	        
    a. Every node has 0 or 2 children	                        
    b. Appears in recursive problems
3. Complete Binary Tree	    
    a. All levels full, last level left-aligned	            
    b. Basis of heaps
4. Perfect Binary Tree	    
    a. All nodes have 2 children & all leaves are at the same level	
    b. Good for theoretical depth questions
5. Balanced Binary Tree	
    a. Height is O(log n)	
    b. Ensures efficient operations
6. Binary Search Tree (BST)	
    a. Left < Root < Right	
    b. Fast search/insert/delete
7. AVL Tree / Red-Black Tree	
    a. Self-balancing BSTs	
    b. Guarantees balanced height
8. Heap (Min/Max)	
    a. CBT with heap property	
    b. Used in priority queues, Dijkstra
9. Trie	
    a. Prefix tree for strings	
    b. Fast autocomplete, word search
10. Segment Tree	
    a. Range queries and updates	
    b. Competitive coding, interval trees
11. Fenwick Tree (BIT)	
    a. Efficient prefix sums	
    b. Space-optimized range queries
12. N-ary Tree	
    a. Each node has ≥ 2 children	
    b. For tree-like JSON, DOMs
13. Suffix Tree	
    a. Built on strings	
    b. Fast substring queries
'''

from __future__ import annotations

class TreeNode:
    def __init__(self, data: str):
        self.data: str = data
        self.children: list[TreeNode] = []
        self.parent: TreeNode = None
    
    def add_child(self, child: TreeNode) -> None:
        child.parent = self
        self.children.append(child)   

    def print_tree(self) -> None:
        print(self.data)
        for child in self.children:
            if child.children:
                child.print_tree()
            else:
                print(child.data)

tree = TreeNode("ROOT")

electronics = TreeNode("ELECTRONICS")

laptop = TreeNode("Laptop")
laptop.add_child(TreeNode("MAC"))
laptop.add_child(TreeNode("INTEL"))
laptop.add_child(TreeNode("ACER"))

electronics.add_child(laptop)
tree.add_child(electronics)

furniture= TreeNode("FURNITURE")
tree.add_child(furniture)

toys = TreeNode("TOYS")
tree.add_child(toys)

tree.print_tree()

print("PROGRAM ENDS")