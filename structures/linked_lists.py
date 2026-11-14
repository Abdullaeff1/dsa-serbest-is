"""Singly and Doubly Linked List implementations (topic 2)."""


class SinglyNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class DoublyNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None


class SinglyLinkedList:
    """Linked list with only a next pointer on each node."""

    def __init__(self):
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def insert_front(self, value):
        """O(1) insert at the beginning."""
        node = SinglyNode(value)
        node.next = self.head
        self.head = node
        self._size += 1

    def insert_back(self, value):
        """O(n) insert at the end (must walk the list)."""
        node = SinglyNode(value)
        if self.head is None:
            self.head = node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = node
        self._size += 1

    def delete_front(self):
        """O(1) remove from the beginning."""
        if self.head is None:
            raise IndexError("list is empty")
        value = self.head.value
        self.head = self.head.next
        self._size -= 1
        return value

    def delete_back(self):
        """O(n) remove from the end."""
        if self.head is None:
            raise IndexError("list is empty")
        if self.head.next is None:
            value = self.head.value
            self.head = None
            self._size -= 1
            return value
        current = self.head
        while current.next.next is not None:
            current = current.next
        value = current.next.value
        current.next = None
        self._size -= 1
        return value

    def search(self, value):
        """Return True if value exists."""
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result


class DoublyLinkedList:
    """Linked list with prev and next pointers; keeps a tail reference."""

    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def insert_front(self, value):
        """O(1) insert at the beginning."""
        node = DoublyNode(value)
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
        self._size += 1

    def insert_back(self, value):
        """O(1) insert at the end thanks to the tail pointer."""
        node = DoublyNode(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1

    def delete_front(self):
        """O(1) remove from the beginning."""
        if self.head is None:
            raise IndexError("list is empty")
        value = self.head.value
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        self._size -= 1
        return value

    def delete_back(self):
        """O(1) remove from the end."""
        if self.tail is None:
            raise IndexError("list is empty")
        value = self.tail.value
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        self._size -= 1
        return value

    def search(self, value):
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result
