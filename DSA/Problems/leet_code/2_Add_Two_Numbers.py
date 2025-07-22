from typing import Optional

'''
Medium
You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

Example 1:

IMG = assets/2_addtwonumber.jpg

Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807.
Example 2:

Input: l1 = [0], l2 = [0]
Output: [0]
Example 3:

Input: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
Output: [8,9,9,9,0,0,0,1]

Constraints:

a. The number of nodes in each linked list is in the range [1, 100].
b. 0 <= Node.val <= 9
c. It is guaranteed that the list represents a number that does not have leading zeros.

'''

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
        
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        currNode1: ListNode | None = l1
        currNode2: ListNode | None = l2
        resultNode = ListNode()
        num = 0
        while currNode1 is not None and currNode2 is not None:
            num = currNode1.val + currNode2.val
            left_num = num // 10
            right_num = num % 10
            resultNode.val = right_num
            resultNode.next = ListNode(val=left_num)
            if currNode1.next is None:
                break
            if currNode2.next is None:
                break
            currNode1 = currNode1.next
            currNode2 = currNode2.next
            
        print(num)