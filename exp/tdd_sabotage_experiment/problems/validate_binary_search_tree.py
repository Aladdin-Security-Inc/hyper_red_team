# problems/validate_binary_search_tree.py

problem_description = """
Given the root of a binary tree, determine if it is a valid binary search tree (BST).

A valid BST is defined as follows:
- The left subtree of a node contains only nodes with keys less than the node's key.
- The right subtree of a node contains only nodes with keys greater than the node's key.
- Both the left and right subtrees must also be binary search trees.

Example 1:
Input: root = [2,1,3]
Output: true

Example 2:
Input: root = [5,1,4,null,null,3,6]
Output: false
Explanation: The root node's value is 5 but its right child's value is 4.
"""

test_code = """
import pytest
from solution import Solution, TreeNode

# Helper function to build a tree from a list for testing
def build_tree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while i < len(values):
        current = queue.pop(0)
        if values[i] is not None:
            current.left = TreeNode(values[i])
            queue.append(current.left)
        i += 1
        if i < len(values) and values[i] is not None:
            current.right = TreeNode(values[i])
            queue.append(current.right)
        i += 1
    return root

def test_simple_valid_bst():
    root = build_tree([2, 1, 3])
    solver = Solution()
    assert solver.isValidBST(root) == True, "Failed on a simple valid BST"

def test_invalid_bst_simple():
    root = build_tree([5, 1, 4, None, None, 3, 6])
    solver = Solution()
    assert solver.isValidBST(root) == False, "Failed on a simple invalid BST"

def test_root_only():
    root = build_tree([1])
    solver = Solution()
    assert solver.isValidBST(root) == True, "Failed on a single-node tree"

def test_empty_tree():
    root = build_tree([])
    solver = Solution()
    assert solver.isValidBST(root) == True, "Failed on an empty tree"

def test_more_complex_valid_bst():
    root = build_tree([10, 5, 15, None, None, 6, 20])
    solver = Solution()
    assert solver.isValidBST(root) == False, "Failed on a more complex invalid BST where right subtree violates constraint"

def test_left_subtree_violation():
    root = build_tree([3, 1, 5, 0, 2, 4, 6])
    # Add a node that violates the BST property deeply
    root.left.right.right = TreeNode(4) # 2's right child cannot be 4 (must be < 3)
    solver = Solution()
    assert solver.isValidBST(root) == False, "Failed on a deep left subtree violation"
"""
