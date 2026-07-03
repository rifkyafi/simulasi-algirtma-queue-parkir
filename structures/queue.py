from structures.node import Node


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        new_node = Node(data)
        if self.rear is None:
            self.front = self.rear = new_node
            return
        self.rear.next = new_node
        self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        return temp.data

    def peek(self):
        if self.front is None:
            return None
        return self.front.data

    def display(self):
        result = []
        current = self.front
        while current:
            result.append(current.data)
            current = current.next
        return result

    def is_empty(self):
        return self.front is None

    def size(self):
        count = 0
        current = self.front
        while current:
            count += 1
            current = current.next
        return count
