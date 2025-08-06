from typing import Optional

"""
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

is_solutions_done = False
is_better_alternative_found = None

"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def print_ll(ll: ListNode):
    curr = ll
    while curr is not None:
        print(curr.val, end=" -> ")
        curr = curr.next
    print("None")


def list_to_nodes(ls):
    head = ListNode(int(ls[0]))
    curr = head
    for i in ls[1:]:
        curr.next = ListNode(int(i))
        curr = curr.next
    return head


class Solution:
    def nodes_to_num(self, ll: ListNode):
        num_str = ""
        curr = ll
        while curr is not None:
            num_str += str(curr.val)
            curr = curr.next
        return int(num_str[::-1])

    is_added = False

    def addTwoNumbers(
        self, l1: Optional[ListNode], l2: Optional[ListNode]
    ) -> Optional[ListNode]:

        # brute force method
        # if l1 is None and l2 is None:
        #     return None
        # if l1 is None:
        #     return l2
        # if l2 is None:
        #     return l1
        # ls1 = self.nodes_to_num(l1)
        # ls2 = self.nodes_to_num(l2)

        # rs = str(ls1 + ls2)
        # rs_reversed_list = list(reversed(rs))

        # head = ListNode(int(rs_reversed_list[0]))
        # curr = head
        # for i in rs_reversed_list[1:]:
        #     curr.next = ListNode(int(i))
        #     curr = curr.next
        # return head
        #
        # Linked List method
        if l1 is None and l2 is None:
            return None
        if l1 is None:
            return l2
        if l2 is None:
            return l1

        head_node = ListNode(l1.val + l2.val)
        curr_node = head_node.next
        l1 = l1.next
        l2 = l2.next
        while l1 is not None and l2 is not None:
            curr_node = ListNode(l1.val + l2.val)
            l1 = l1.next
            l2 = l2.next
            curr_node = curr_node.next
        if l1 is None:
            curr_node = l2
        if l2 is None:
            curr_node = l2

        return head_node


ls1 = list_to_nodes([2, 4, 3])
ls2 = list_to_nodes([5, 6, 4])

# print_ll(ls1)
# print_ll(ls2)

sol = Solution()
node_result = sol.addTwoNumbers(ls1, ls2)

print_ll(node_result)
