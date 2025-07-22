class Queue:
    '''
    Queue follows FIFO Principle like a queue of people ordering food in a line.
    '''
    def __init__(self):
        self.queue = []
        
    def enqueue(self, data):
        self.queue.append(data)
    
    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        return None
    
    def is_empty(self):
        return self.size() == 0
    
    def size(self):
        return len(self.queue)
    
    
class CirclularQueue:
    '''
    A Circular Queue is a linear data structure that follows FIFO, but the last position is connected back to the first position, forming a circle.
    It reuses empty spaces left by dequeued elements — unlike regular queue where space is wasted when elements are removed from front.
    '''
    def __init__(self, capacity:int):
        self.queue = []
        self.capacity:int = capacity
        self.front:int = -1
        self.rear:int = -1
    
    def enqueue(self, data):
        if self.is_full():
            return "Queue is full!"
        if self.is_empty():
            self.front = 0
        self.rear = (self.rear + 1) % self.capacity
        self.queue[self.rear] = data
    
    def dequeue(self):
        if self.is_empty():
            return "Queue is empty!"
        removed = self.queue[self.front]
        self.queue[self.front] = None
        if self.front == self.rear:
            self.front = self.rear = -1
        else:
            self.front = ( self.front + 1 ) % self.capacity
        return removed
    
    def peek(self):
        if self.is_empty():
            return "Queue is empty!"
        return self.queue[self.front]
    
    def display(self):
        pass
    
    def is_empty(self):
        pass

    def is_full(self):
        pass
    
    def size(self):
        pass
    