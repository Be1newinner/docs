'''
Hash Map using linked list
'''

class Node:
    def __init__(self, key, value):
        self.value = value
        self.key = key
        self.next = None
        
class HashMap:
    def __init__(self, size: int):
        self.size: int = size
        self.buckets: list[any] = [None] * size
        
    def _hash(self, key):
        return hash(key) % self.size
    
    def put(self, key, value):
        index = self._hash(key)
        head = self.buckets[index]
        
        current = head
        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next
        
        # if key doesn't exists
        new_node = Node(key, value)
        new_node.next = head
        self.buckets[index] = new_node
        
    def get(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        
        while current:
            if current.key == index:
                return current.value
            current = current.next
        return None
    
    def remove(self, key):
        index = self._hash(key)
        current = self.buckets[index]
        prev = None
        
        while current:
            if current.key == key:
                if prev:
                    prev.next = current.next
                else:
                    self.buckets[index] = current.next
                return True
            prev = current
            current = current.next
        return False