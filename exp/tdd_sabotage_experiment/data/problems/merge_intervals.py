# problems/merge_intervals.py

problem_description = """
Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals,
and return an array of the non-overlapping intervals that cover all the intervals in the input.

Example 1:
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].

Example 2:
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.
"""

test_code = """
import pytest
from solution import Solution

def test_example_1():
    intervals = [[1,3],[2,6],[8,10],[15,18]]
    expected = [[1,6],[8,10],[15,18]]
    solver = Solution()
    assert sorted(solver.merge(intervals)) == sorted(expected), "Failed on example 1"

def test_example_2():
    intervals = [[1,4],[4,5]]
    expected = [[1,5]]
    solver = Solution()
    assert sorted(solver.merge(intervals)) == sorted(expected), "Failed on example 2"

def test_no_overlap():
    intervals = [[1,2],[3,4],[5,6]]
    expected = [[1,2],[3,4],[5,6]]
    solver = Solution()
    assert sorted(solver.merge(intervals)) == sorted(expected), "Failed on non-overlapping intervals"

def test_all_overlap():
    intervals = [[1,5],[2,4],[3,6]]
    expected = [[1,6]]
    solver = Solution()
    assert sorted(solver.merge(intervals)) == sorted(expected), "Failed on all-overlapping intervals"

def test_single_interval():
    intervals = [[1,10]]
    expected = [[1,10]]
    solver = Solution()
    assert sorted(solver.merge(intervals)) == sorted(expected), "Failed on a single interval"

def test_empty_input():
    intervals = []
    expected = []
    solver = Solution()
    assert sorted(solver.merge(intervals)) == sorted(expected), "Failed on empty input"
"""
