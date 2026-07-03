from structures.bst_node import BSTNode


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if self.root is None:
            self.root = BSTNode(key, data)
            return
        self._insert_rec(self.root, key, data)

    def _insert_rec(self, node, key, data):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, data)
            else:
                self._insert_rec(node.left, key, data)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, data)
            else:
                self._insert_rec(node.right, key, data)
        else:
            node.data = data

    def search(self, key):
        return self._search_rec(self.root, key)

    def _search_rec(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node
        if key < node.key:
            return self._search_rec(node.left, key)
        return self._search_rec(node.right, key)

    def delete(self, key):
        self.root, deleted = self._delete_rec(self.root, key)
        return deleted

    def _delete_rec(self, node, key):
        if node is None:
            return None, None
        if key < node.key:
            node.left, deleted = self._delete_rec(node.left, key)
            return node, deleted
        if key > node.key:
            node.right, deleted = self._delete_rec(node.right, key)
            return node, deleted
        deleted = node.data
        if node.left is None:
            return node.right, deleted
        if node.right is None:
            return node.left, deleted
        min_node = self._min_value_node(node.right)
        node.key = min_node.key
        node.data = min_node.data
        node.right, _ = self._delete_rec(node.right, min_node.key)
        return node, deleted

    def _min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def inorder(self):
        result = []
        self._inorder_rec(self.root, result)
        return result

    def _inorder_rec(self, node, result):
        if node:
            self._inorder_rec(node.left, result)
            result.append((node.key, node.data))
            self._inorder_rec(node.right, result)

    def is_empty(self):
        return self.root is None
