# Definition for singly-linked list.
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverseBetween(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
    values = []
    nodes = []
    curr = head
    while curr:
        if left <= 1 and right >= 1:
            values.append(curr.val)
            nodes.append(curr)
        curr = curr.next
        left -= 1
        right -= 1
    for node in nodes:
        node.val = values.pop(-1)
    return head


head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
a = reverseBetween(head, 2, 4)
print(a)