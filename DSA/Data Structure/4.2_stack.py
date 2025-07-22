class Stack:
    '''
    Stack follows LIFO principle: Last In Fist Out.
    The item which is pushed at last will be popped first.
    these are basic methods of stack
    '''
    def __init__(self):
        self.stack = []
        
    def push(self, data):
        self.stack.append(data)
    
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None
    
    def seek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def size(self):
        return len(self.stack)