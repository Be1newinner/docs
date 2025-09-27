"""
You are given the heads of two sorted linked lists list1 and list2.

Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

Return the head of the merged linked list.

Example 1:

https://assets.leetcode.com/uploads/2020/10/03/merge_ex1.jpg

Input: list1 = [1,2,4], list2 = [1,3,4]
Output: [1,1,2,3,4,4]
Example 2:

Input: list1 = [], list2 = []
Output: []
Example 3:

Input: list1 = [], list2 = [0]
Output: [0]


Constraints:

The number of nodes in both lists is in the range [0, 50].
-100 <= Node.val <= 100
Both list1 and list2 are sorted in non-decreasing order.
"""

from typing import Optional


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def mergeTwoLists(
        self, list1: Optional[ListNode], list2: Optional[ListNode]
    ) -> Optional[ListNode]:
        head_node = ListNode()  # Dummy head Node
        curr_node = head_node

        while list1 is not None and list2 is not None:
            if list1.val < list2.val:
                curr_node.next = list1
                list1 = list1.next
            else:
                curr_node.next = list2
                list2 = list2.next
            curr_node = curr_node.next

        if list1 is None or list2 is None:
            if list1 is None:
                curr_node.next = list2
                curr_node = curr_node.next
            else:
                curr_node.next = list1
                curr_node = curr_node.next

        # Removing dummy node
        head_node = head_node.next
        return head_node


def list_to_linked_list(ls: list):
    head_node = ListNode(ls[0])
    curr = head_node
    for i in ls[1:]:
        curr.next = ListNode(i)
        curr = curr.next
    return head_node


list1 = [1, 2, 4]
list2 = [1, 3, 4]
# Output = [1,1,2,3,4,4]

nodes1 = list_to_linked_list(list1)
nodes2 = list_to_linked_list(list2)

sol = Solution()
merged_linked_list = sol.mergeTwoLists(nodes1, nodes2)
print(merged_linked_list)
