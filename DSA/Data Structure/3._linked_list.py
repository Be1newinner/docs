
# Linked List => A LInear Data Structure where each node points to its next node.

# Single Linked List => Here Each node has data and next value reference

class Node:
    def __init__(self, value):
        self.data = value
        self.next = None 
        
class SingleLinkedList:
    def __init__(self):
        self.head = None
        
    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node
        
    def print_list(self):
        curr = self.head
        while curr:
            print(curr.data, end=" => ")
            curr = curr.next
        print("None")
    
    def delete_node_by_data(self,data):
        curr = self.data
        prev = None
        while curr and curr.data != data:
            prev = curr
            curr = curr.next
        if not curr:
            return False # means data was not found
        if not prev:
            self.head = curr
        else:
            59
        curr.next= temp2
        

def reverse_single_list(head):
    prev = None
    curr = head
    while curr:                     
        nxt = curr.next             
        curr.next = prev            
        prev = curr                 
        curr = nxt        

# Flyod or (Tortorise and hare algorithm) 
def check_single_list_cycle(head):
    fast = slow = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False    
   
class DNode:
    def __init__(self, data):
        self.data = data   
        self.next = None
        self.prev = None
     
class DoublyLinkedList:
    def __init__(self):
        self.head = None
            
    def insert_at_end(self, data):
        '''
        we will check if the head is empty if yes then insert at head;
        self.head = data
        else:
        add data just as we do in single linked list
        '''
        new_node = DNode(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node
        new_node.prev = curr
        
    def insert_at_start(self, data):
        '''
        if head is empty insert data at head else
        insert at prev of head which is O(1)
        '''
        new_node = DNode(data)
        if self.head:
            self.head.prev = new_node
            new_node.next= self.head
        self.head = new_node
    
    def print_forward(self):
        curr = self.head
        while curr:
            print(curr.data, end=" => ")
            curr = curr.next
        print("None")
        
    def print_backward(self):
        curr= self.head
        while curr.next:
            curr = curr.next
        while curr:
            print(curr.data, end=" => ")
            curr = curr.prev
        print("None")
            
    def delete_node_by_data(self,data):
        curr = self.data
        while curr and curr.data != data:
            curr = curr.next
        if not curr:
            return False
        if curr.prev:
            curr.prev.next = curr.next
        else:
            self.head = curr.next 
        if curr.next:
            curr.next.prev = curr.prev
        return True
        
# Usage
ls = SingleLinkedList()
ls.insert_at_end("Hi")
ls.insert_at_end("Bye")
ls.insert_at_end("Nye")
ls.insert_at_end("Dye")
ls.insert_at_end("Fye")

ls.print_list()