"""Custom Hash Table with separate chaining (topic 4)."""


class HashTable:
    """Simple hash table: each bucket is a Python list of (key, value) pairs."""

    def __init__(self, capacity=8):
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0
        self._load_factor_threshold = 0.75

    def __len__(self):
        return self._size

    def _hash(self, key):
        """Map key to a bucket index. Uses Python hash, then modulo."""
        return abs(hash(key)) % self._capacity

    def _resize(self):
        """Double capacity and re-insert all pairs."""
        old_items = self.items()
        self._capacity *= 2
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0
        for key, value in old_items:
            self.put(key, value)

    def put(self, key, value):
        """Insert or update key -> value. Average O(1)."""
        if (self._size + 1) / self._capacity > self._load_factor_threshold:
            self._resize()
        index = self._hash(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1

    def get(self, key, default=None):
        """Return value for key, or default if missing."""
        index = self._hash(key)
        for k, v in self._buckets[index]:
            if k == key:
                return v
        return default

    def contains(self, key):
        index = self._hash(key)
        for k, _ in self._buckets[index]:
            if k == key:
                return True
        return False

    def remove(self, key):
        """Remove key. Raises KeyError if not found."""
        index = self._hash(key)
        bucket = self._buckets[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return
        raise KeyError(key)

    def items(self):
        result = []
        for bucket in self._buckets:
            result.extend(bucket)
        return result

    def collision_count(self):
        """How many buckets currently hold more than one pair."""
        return sum(1 for b in self._buckets if len(b) > 1)
