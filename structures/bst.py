"""Binary Search Tree and helpers for balance analysis (topic 5)."""


class BSTNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """Simple BST: left < node < right. No self-balancing."""

    def __init__(self):
        self.root = None
        self._size = 0

    def __len__(self):
        return self._size

    def insert(self, value):
        """Insert value. Duplicates are ignored."""
        if self.root is None:
            self.root = BSTNode(value)
            self._size = 1
            return
        current = self.root
        while True:
            if value == current.value:
                return
            if value < current.value:
                if current.left is None:
                    current.left = BSTNode(value)
                    self._size += 1
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = BSTNode(value)
                    self._size += 1
                    return
                current = current.right

    def search(self, value):
        current = self.root
        while current is not None:
            if value == current.value:
                return True
            if value < current.value:
                current = current.left
            else:
                current = current.right
        return False

    def _min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def delete(self, value):
        """Delete value if present. Returns True if deleted."""
        self.root, deleted = self._delete_rec(self.root, value)
        if deleted:
            self._size -= 1
        return deleted

    def _delete_rec(self, node, value):
        if node is None:
            return None, False
        if value < node.value:
            node.left, deleted = self._delete_rec(node.left, value)
            return node, deleted
        if value > node.value:
            node.right, deleted = self._delete_rec(node.right, value)
            return node, deleted
        # Found the node to delete.
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True
        successor = self._min_node(node.right)
        node.value = successor.value
        node.right, _ = self._delete_rec(node.right, successor.value)
        return node, True

    def height(self):
        """Tree height. Empty tree has height -1; single node has height 0.

        Uses an iterative level walk so deep (unbalanced) trees do not
        hit Python's recursion limit.
        """
        if self.root is None:
            return -1
        height = -1
        level = [self.root]
        while level:
            height += 1
            next_level = []
            for node in level:
                if node.left is not None:
                    next_level.append(node.left)
                if node.right is not None:
                    next_level.append(node.right)
            level = next_level
        return height

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node.value)
        self._inorder(node.right, result)
