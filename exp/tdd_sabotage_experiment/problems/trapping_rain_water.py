# problems/trapping_rain_water.py

problem_description = """
Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

Example 1:
Input: height = [0,1,0,2,1,0,1,3,2,1,2,1]
Output: 6
Explanation: The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

Example 2:
Input: height = [4,2,0,3,2,5]
Output: 9
"""

test_code = """
import pytest
from solution import Solution

def test_example_1():
    height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
    solver = Solution()
    assert solver.trap(height) == 6, "Failed on example 1"

def test_example_2():
    height = [4, 2, 0, 3, 2, 5]
    solver = Solution()
    assert solver.trap(height) == 9, "Failed on example 2"

def test_empty_list():
    height = []
    solver = Solution()
    assert solver.trap(height) == 0, "Failed on an empty list"

def test_no_trapped_water():
    height = [1, 2, 3, 4, 5]
    solver = Solution()
    assert solver.trap(height) == 0, "Failed on a monotonically increasing list"

def test_bowl_shape():
    height = [5, 1, 1, 1, 5]
    solver = Solution()
    assert solver.trap(height) == 12, "Failed on a simple bowl shape"

def test_complex_terrain():
    height = [6, 4, 2, 0, 3, 2, 0, 3, 1, 4, 5, 3, 2, 7, 5, 3, 0, 1, 2, 1, 3, 4, 6, 8, 1, 3]
    solver = Solution()
    assert solver.trap(height) == 83, "Failed on a complex terrain"
"""
