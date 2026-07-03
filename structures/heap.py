class MaxHeap:
    def __init__(self):
        self.heap = []

    def insert(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        max_item = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return max_item

    def peek(self):
        if not self.heap:
            return None
        return self.heap[0]

    def _heapify_up(self, idx):
        parent = (idx - 1) // 2
        if idx > 0 and self.heap[idx][0] > self.heap[parent][0]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            self._heapify_up(parent)

    def _heapify_down(self, idx):
        largest = idx
        left = 2 * idx + 1
        right = 2 * idx + 2
        if left < len(self.heap) and self.heap[left][0] > self.heap[largest][0]:
            largest = left
        if right < len(self.heap) and self.heap[right][0] > self.heap[largest][0]:
            largest = right
        if largest != idx:
            self.heap[idx], self.heap[largest] = self.heap[largest], self.heap[idx]
            self._heapify_down(largest)

    def display(self):
        return self.heap[:]

    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)
