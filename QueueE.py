import threading
from threading import Semaphore

class QueueE: 
    def __init__(self, capacity = 10):
        self.queue = [] 
        self.capacity = capacity
        self.semaphoreCapacity = threading.Semaphore(capacity)
        self.semaphoreUsed = threading.Semaphore(0)

    def enqueue(self, item):
        self.semaphoreCapacity.acquire()
        self.queue.append(item)
        self.semaphoreUsed.release()

    def dequeue(self):
        self.semaphoreUsed.acquire()
        item = self.queue.pop(0)
        self.semaphoreCapacity.release()
        return item

    def peek(self):
        return self.queue[0]
