"""Fixed-capacity Array and Dynamic Array (topic 1).

Comments are in English as agreed for the team project.
"""


class FixedArray:
    """Array with a fixed maximum capacity."""

    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._data = [None] * capacity
        self._size = 0

    def __len__(self):
        return self._size

    @property
    def capacity(self):
        return self._capacity

    def is_full(self):
        return self._size >= self._capacity

    def is_empty(self):
        return self._size == 0

    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        return self._data[index]

    def set(self, index, value):
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        self._data[index] = value

    def append(self, value):
        """Add value at the end. Raises error if capacity is full."""
        if self.is_full():
            raise OverflowError("fixed array is full")
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        """Insert value at index, shifting elements to the right."""
        if self.is_full():
            raise OverflowError("fixed array is full")
        if index < 0 or index > self._size:
            raise IndexError("index out of range")
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def remove_at(self, index):
        """Remove and return element at index, shifting left."""
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._size -= 1
        self._data[self._size] = None
        return value

    def search(self, value):
        """Linear search. Returns index or -1 if not found."""
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1

    def to_list(self):
        return self._data[: self._size]


class DynamicArray:
    """Resizable array that grows by doubling capacity when full."""

    def __init__(self, initial_capacity=4):
        if initial_capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = initial_capacity
        self._data = [None] * initial_capacity
        self._size = 0

    def __len__(self):
        return self._size

    @property
    def capacity(self):
        return self._capacity

    def is_empty(self):
        return self._size == 0

    def get(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        return self._data[index]

    def set(self, index, value):
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        self._data[index] = value

    def _resize(self, new_capacity):
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity

    def append(self, value):
        """Add at the end. Amortized O(1) because of doubling."""
        if self._size >= self._capacity:
            self._resize(self._capacity * 2)
        self._data[self._size] = value
        self._size += 1

    def insert(self, index, value):
        """Insert at index. May trigger a resize."""
        if index < 0 or index > self._size:
            raise IndexError("index out of range")
        if self._size >= self._capacity:
            self._resize(self._capacity * 2)
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        self._data[index] = value
        self._size += 1

    def remove_at(self, index):
        """Remove at index. Shrinks when size is 1/4 of capacity."""
        if index < 0 or index >= self._size:
            raise IndexError("index out of range")
        value = self._data[index]
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        self._size -= 1
        self._data[self._size] = None
        # Keep at least capacity 4 to avoid tiny arrays.
        if self._size > 0 and self._size * 4 <= self._capacity and self._capacity > 4:
            new_cap = max(4, self._capacity // 2)
            self._resize(new_cap)
        return value

    def search(self, value):
        """Linear search. Returns index or -1."""
        for i in range(self._size):
            if self._data[i] == value:
                return i
        return -1

    def to_list(self):
        return self._data[: self._size]
