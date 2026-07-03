from structures.node import Node


class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        temp = self.top
        self.top = self.top.next
        return temp.data

    def peek(self):
        if self.top is None:
            return None
        return self.top.data

    def display(self):
        result = []
        current = self.top
        while current:
            result.append(current.data)
            current = current.next
        return result

    def is_empty(self):
        return self.top is None

    def size(self):
        count = 0
        current = self.top
        while current:
            count += 1
            current = current.next
        return count
