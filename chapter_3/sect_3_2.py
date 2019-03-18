#!/usr/bin/env python
# -*- encoding:UTF-8 -*-
import doctest
import random
import collections

class TreeNode(object):
    def __init__(self, key, val, size):
        self._left = self._right = None
        self._val = val
        self._size = size

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        assert isinstance(node, (Node, type(None)))
        self._left = node

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        assert isinstance(node, (Node, type(None)))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, val):
        assert isinstance(val, int) and val >= 0
        self._size = val

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, val):
        self._key = val

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, value):
        self._val = value 

class BST(object):
    """
      Binary search tree implementation.
    >>> bst = BST()
    >>> bst.is_empty()
    True
    >>> test_str = 'EASYQUESTION'
    >>> for (index, element) in enumerate(test_str):
    ...     bst.put(element, index)
    ...
    >>> bst.is_binary_tree()
    True
    >>> bst.get('Q')
    4
    >>> bst.get('E')
    6
    >>> bst.get('N')
    11
    >>> bst.size()
    10
    >>> bst.max_val().key
    'Y'
    >>> bst.min_val().key
    'A'
    >>> bst.select(0).key
    'A'
    >>> bst.select(3).key
    'N'
    >>> bst.select(4).key
    'O'
    >>> bst.select(9).key
    'Y'
    >>> bst.rank('A')
    0
    >>> bst.rank('E')
    1
    >>> bst.rank('Y')
    9
    >>> bst.rank('T')
    7
    >>> bst.rank('U')
    8
    >>> bst.is_empty()
    False
    >>> node = bst.select(0)
    >>> node.key
    'A'
    >>> node2 = bst.select(2)
    >>> node2.key
    'I'
    >>> node3 = bst.select(9)
    >>> node3.key
    'Y'
    >>> bst.keys()
    ['A', 'E', 'I', 'N', 'O', 'Q', 'S', 'T', 'U', 'Y']
    >>> bst.height()
    5
    >>> random_key = bst.random_key()
    >>> random_key in test_str
    True
    >>> fn = bst.floor('B')
    >>> fn.key
    'A'
    >>> fn2 = bst.floor('Z')
    >>> fn2.key
    'Y'
    >>> fn3 = bst.floor('E')
    >>> fn3.key
    'E'
    >>> cn = bst.ceiling('B')
    >>> cn.key
    'E'
    >>> cn2 = bst.ceiling('R')
    >>> cn2.key
    'S'
    >>> cn3 = bst.ceiling('S')
    >>> cn3.key
    'S'
    >>> bst.delete_min()
    >>> bst.min_val().key
    'E'
    >>> bst.delete_max()
    >>> bst.max_val().key
    'U'
    >>> bst.delete('O')
    >>> bst.delete('S')
    >>> bst.keys()
    ['E', 'I', 'N', 'Q', 'T', 'U']
    >>> bst.is_binary_tree()
    True
    >>> bst.is_ordered()
    True
    >>> bst.is_rank_consistent()
    True
    >>> bst.check()
    True
    """

    def __init__(self):
        self._root = None

    def size(self):
        """
        Return the size of the BST rooted at node
        """
        if not self._root:
            return 0
        return self._root.size

    def is_empty(self):
        return self._root is None

    def node_size(self, node):
        """Get the size of subtree rooted at node. Could be None"""
        if not node:
            return 0
        else:
            return node.size

    def get(self, key):
        """returns the value association with a key. If key is not in ST, return None"""
        if not key:
            raise ValueError("Illegal key")

        return self._get(self._root, key)

          
    def _get(self, node, key):
        """Helper function to recurse on node of tree"""
        # Base case
        if not node: return None

        if node.key < key:
            return self._get(node.left, key)
        elif node.key > key:
            return self._get(node.right, key)
        else:
            return node.val

    def put(self, key, val):
        """Insert the key-val pair into the symbol table"""
        if not key: raise ValueError("Illegal key")
        if not val:
            self.delete(key)
            return

        # Need treenode update as we go for size tracking
        self._root = self._put(self._root, key, val)

        # Check for BST property
        assert self.is_binary_tree()

    def _put(self, node, key, val):
        # Base case, simply make a new node and return
        if not node:
           return TreeNode(key, val, 1) 

        # Recursion
        if node.key < key: # Update the left child tree
            node.left = self._put(node.left, key, val)
        elif node.key > key: # Update the right tree
            node.right = self._put(node.right, key, val)
        else:   # Found the node to update
            node.val = val

        # Left or right subtree might have been updated, update my size as well
        node.size = 1 + self.node_size(node.left) + self.node_size(node.right) 

        return node

    # 3.2.29 practice, check if each node's size is
    # equals to the summation of left node's size and right node's size.
    def is_binary_tree(self):
        return self.__is_binary_tree(self._root)

    def __is_binary_tree(self, node):
        if not node:
            return True
        if node.size != self.node_size(node.left) + self.node_size(node.right) + 1:
            return False
        return self.__is_binary_tree(node.left) and self.__is_binary_tree(node.right)

    # 3.2.30 practice: Check if each node is BST is ordered
    # (less than right node / greater than left node)
    def is_ordered(self):
        return self._is_ordered(self._root, None, None)

    def _is_ordered(self, node, min_key, max_key):
        # Base case
        if not node: return True

        # Check
        if min_key and node.val < min_key: return False
        if max_key and node.val > max_key: return False

        # Recurse
        return self._is_ordered(node.left, min_key, node.val) and self._is_ordered(node.right, node.val, max_key)

    # 3.2.14 practice: implement these methods
    def max_val(self):
        """Find the max val contained in the BST"""
        return self._max_val(self._root, None)

    def _max_val(self, node, max_val):
        if not node:
            return max_val

        if not max_val or node.val > max_val:   # Propagate node.val
            return max(self._max_val(node.left, node.val), self._max_val(node.right, node.val))
        else:   # Propage max_val
            return max(self._max_val(node.left, max_val), self._max_val(node.right, max_val))

    # 3.2.14 practice
    def min_val(self):
        """Find the minimum value in the BST"""
        return self._min_val(self._root, None)

    def _min_val(self, node, min_val):
        if not node:
            return min_val

        if not min_val or node.val < min_val:   # Propage node.val
            return min(self._min_val(node.left, node.val), self._min_val(node.right, node.val))
        else:   # Propage min_val
            return min(self._min_val(node.left, min_val), self._min_val(node.right, min_val))

    def min_node(self):
        """Returns the min node in the BST"""
        return self._min_node(self._root)

    def _min_node(self, node):
        if not node:
            return None

        # Traverse of left-most leave node
        while node.left:
            node = node.left

        return node

    def max_node(self):
        return self._max_node(self._root)

    def _max_node(self, node):
        if not node:
            return None

        while node.right:
            node = node.right
        return node

    def max_key(self):
        """Find the max key in the BST"""
        if not self._root:
            return None

        node = self._root

        while node.right:
            node = node.right

        return node.key


    def min_key(self):
        """Find the min key in the BST"""
        if not self._root:
            return None

        node = self._root

        while node.left:
            node = node.left

        return node.key

    # 3.2.14 practice
    def select(self, k):
        """Find the kth node of the BST"""
        num_lt = k-1
        node = self._root

        while node:
            if self.node_size(node.left) == num_lt:
                num_lt = 0
                break
            elif self.node_size(node.left) > num_lt:
                node = node.left
            else:
                num_lt = num_lt - self.node_size(node.left) - 1
                node = node.right

        if num_lt > 0:
            return None
        else:
            return node

    # 3.2.14 practice:
    def rank(self, key):
        """Find the rank of the node in BST by the given key"""
        return self._rank(self._root, key)

    def _rank(self, node, key):
        if not node:                            # Base case
            return 0

        if node.val == key:                     # Done recursing
            return self.node_size(node.left)
        elif node.val > key:                    # Recurse left
            return self._rank(node.left, key)
        else:                                   # Recurse right
            return self.node_size(node.left) + 1 + self._rank(node.right, key)


    def rank_iterative(self, key):
        """
        Iterative implementation of rank
        """
        result = 0
        node = self._root 

        while node:
            if node.val == key:
                result += self.node_size(node.left)
                break
            elif node.val > key:    # Go left
                node = node.left
            else:           # Go right
                result =+ self.node_size(node.left) + 1
                node = node.right

        return result

    def delete_min(self):
        """Find the minimum key and delete it"""
        if not self._root:
            return 

        # Start deleting at root
        self._root = self._delete_min(self._root)

    def _delete_min(self, node):
        """Helper routine for recursive impl"""
        # Base case (looking forward) - I'm the min-key node
        if not node.left:
            return node.right

        node.left = self._delete_min(node.left) # Recurse
        node.size = self.node_size(node.left) + self.node_size(node.right) + 1
        return node

    def delete_max(self):
        """Find the maximum key and delete it"""
        if not self._root:
            return

        # Start deleting at root
        self._root = self._delete_max(self._root)

    def _delete_max(self):
        # Base case (looking forward) - I'm the max-key node
        if not node.right:
            return node.left

        node.right = self._delete_max(node.right)
        node.size = self.node_size(node.left) + self.node_size(node.right) + 1

    def delete(self, k):
        """Delete corresponding key k from table"""
        self._root = self._delete(self._root, k)

    def _delete(self, node, k):
        """Helper routine to do recursion"""
        if not node:
            return None

        if node.key > k:
            # Recurse and update left subtree
            node.left = self._delete(node.left, k)
        elif node.key < k:
            # Recurse and update right subtree
            node.right = self._delete(node.right, k)
        else:
            # Replace this node by its successor in linear order
            if not node.left or not node.right:
                return (node.left or node.right)
            tmp = node
            node = self._min_node(tmp.right)
            node.right = self._delete_min(tmp.right) 
            node.left = tmp.left

        # Update size
        node.size = self.size_of(node.left) + self.size_of(node.right) + 1
        return node

    def keys(self):
        """Return an iterable of all nodes on the BST"""
        return self.keys(self.min_node().key, self.max_node().key)

    def keys(self, lo, hi):
        """Returns an iterable of all nodes on BST with between lo and hi""" 
        queue = collections.deque()
        # Starting at root, traverse all nodes on BST and collect in queue
        self._keys(self._root, queue, lo, hi)

    def _keys(self, node, queue, lo, hi):
        """In-order traversal to add nodes to queue"""
        if not node:
            return

        # Traverse left sub-tree if needed to collect nodes in queue
        if lo < node.key:       
            self._keys(node.left, queue, lo, hi) 

        # This node
        if lo <= node.key and node.key <= hi:
            queue.append(node)

        # Traverse right sub-tree if needed
        if node.key < hi:
            self._keys(node.right, queue, lo, hi)

    def level_order():
        """Returns the keys in BST in level order"""
        if not self._root:
            return None

        iter_queue = collections.deque()
        keys = collections.deque()
        iter_queue.append(self._root)

        while not iter_queue: # queue is not empty
            # Get current node
            node = iter_queue.pop_left()
            # Process node
            keys.append(node)
            # Check left and right
            if node.left:
                iter_queue.append(node.left)
            elif node.right:
                iter_queue.append(node.right)

        return keys

    # 3.2.6 practice: add height function for BST
    def height(self):
        """Returns the height of the BST"""
        return self._height(self._root)

    def _height(self, node):
        if not node: # Null node has height -1
            return -1

        # Recurse left and right subtree, then compute height for this node
        return 1 + max(self._height(node.left), self._height(node.right))

        
        


if __name__ == '__main__':
    doctest.testmod()

