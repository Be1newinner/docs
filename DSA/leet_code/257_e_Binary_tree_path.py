"""
Difficulty: Easy
Topic: String, Backtracking, Tree, Depth-First Search, Binary Tree

Given the root of a binary tree, return all root-to-leaf paths in any order.
A leaf is a node with no children.

https://assets.leetcode.com/uploads/2021/03/12/paths-tree.jpg

Input: root = [1,2,3,null,5]
Output: ["1->2->5","1->3"]
Example 2:

Input: root = [1]
Output: ["1"]


Constraints:

The number of nodes in the tree is in the range [1, 100].
-100 <= Node.val <= 100

"""

from typing import Optional, List


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def binaryTreePaths(self, root: Optional[TreeNode]) -> List[str]:
        pass


def list_to_linked_list(ls: list):
    head_node = TreeNode(ls[0])
    curr = head_node
    for i in ls[1:]:
        curr.next = TreeNode(i)
        curr = curr.next
    return head_node


list1 = [1, 2, 3, None, 5]
# Output = ["1->2->5","1->3"]

list2 = [1]
# Output = ["1"]

nodes1 = list_to_linked_list(list1)
nodes2 = list_to_linked_list(list2)

sol = Solution()
merged_linked_list = sol.mergeTwoLists(nodes1, nodes2)
print(merged_linked_list)
