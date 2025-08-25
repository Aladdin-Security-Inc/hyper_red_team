# problems/longest_increasing_subsequence.py

problem_description = """
Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

A subsequence is a sequence that can be derived from an array by deleting some or no elements without changing the order of the remaining elements. For example, [3,6,2,7] is a subsequence of the array [0,3,1,6,2,2,7].

Example 1:
Input: nums = [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

Example 2:
Input: nums = [0,1,0,3,2,3]
Output: 4

Example 3:
Input: nums = [7,7,7,7,7,7,7]
Output: 1
"""

test_code = """
import pytest
from solution import Solution

def test_example_1():
    nums = [10, 9, 2, 5, 3, 7, 101, 18]
    solver = Solution()
    assert solver.lengthOfLIS(nums) == 4, "Failed on example 1"

def test_example_2():
    nums = [0, 1, 0, 3, 2, 3]
    solver = Solution()
    assert solver.lengthOfLIS(nums) == 4, "Failed on example 2"

def test_all_same_elements():
    nums = [7, 7, 7, 7, 7, 7, 7]
    solver = Solution()
    assert solver.lengthOfLIS(nums) == 1, "Failed on all same elements"

def test_already_sorted():
    nums = [1, 2, 3, 4, 5]
    solver = Solution()
    assert solver.lengthOfLIS(nums) == 5, "Failed on an already sorted array"

def test_reverse_sorted():
    nums = [5, 4, 3, 2, 1]
    solver = Solution()
    assert solver.lengthOfLIS(nums) == 1, "Failed on a reverse sorted array"

def test_empty_list():
    nums = []
    solver = Solution()
    assert solver.lengthOfLIS(nums) == 0, "Failed on an empty list"
"""
