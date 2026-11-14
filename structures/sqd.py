"""Stack, Queue and Deque built on simple lists / linked ideas (topic 3)."""

from .linked_lists import DoublyLinkedList
from .array_ops import DynamicArray


class Stack:
    """LIFO stack backed by DynamicArray."""

    def __init__(self):
        self._data = DynamicArray()

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return self._data.is_empty()

    def push(self, value):
        self._data.append(value)

    def pop(self):
        if self.is_empty():
            raise IndexError("stack is empty")
        return self._data.remove_at(len(self._data) - 1)

    def peek(self):
        if self.is_empty():
            raise IndexError("stack is empty")
        return self._data.get(len(self._data) - 1)


class Queue:
    """FIFO queue backed by DoublyLinkedList (O(1) ends)."""

    def __init__(self):
        self._data = DoublyLinkedList()

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return self._data.is_empty()

    def enqueue(self, value):
        self._data.insert_back(value)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        return self._data.delete_front()

    def front(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        return self._data.head.value


class Deque:
    """Double-ended queue: add/remove at both ends in O(1)."""

    def __init__(self):
        self._data = DoublyLinkedList()

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return self._data.is_empty()

    def add_front(self, value):
        self._data.insert_front(value)

    def add_back(self, value):
        self._data.insert_back(value)

    def remove_front(self):
        if self.is_empty():
            raise IndexError("deque is empty")
        return self._data.delete_front()

    def remove_back(self):
        if self.is_empty():
            raise IndexError("deque is empty")
        return self._data.delete_back()

    def to_list(self):
        return self._data.to_list()
