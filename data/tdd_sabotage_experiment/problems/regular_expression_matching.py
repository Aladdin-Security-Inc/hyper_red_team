# problems/regular_expression_matching.py

problem_description = """
Given an input string `s` and a pattern `p`, implement regular expression matching with support for '.' and '*' where:
- '.' Matches any single character.
- '*' Matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

Example 1:
Input: s = "aa", p = "a"
Output: false
Explanation: "a" does not match the entire string "aa".

Example 2:
Input: s = "aa", p = "a*"
Output: true
Explanation: '*' means zero or more of the preceding element, 'a'. Therefore, by repeating 'a' once, it becomes "aa".

Example 3:
Input: s = "ab", p = ".*"
Output: true
Explanation: ".*" means "zero or more of any character".
"""

test_code = """
import pytest
from solution import Solution

def test_example_1():
    s, p = "aa", "a"
    solver = Solution()
    assert solver.isMatch(s, p) == False, "Failed on example 1"

def test_example_2():
    s, p = "aa", "a*"
    solver = Solution()
    assert solver.isMatch(s, p) == True, "Failed on example 2"

def test_example_3():
    s, p = "ab", ".*"
    solver = Solution()
    assert solver.isMatch(s, p) == True, "Failed on example 3"

def test_complex_match():
    s, p = "aab", "c*a*b"
    solver = Solution()
    assert solver.isMatch(s, p) == True, "Failed on a more complex match"

def test_no_match():
    s, p = "mississippi", "mis*is*p*."
    solver = Solution()
    assert solver.isMatch(s, p) == False, "Failed on a non-matching case"

def test_empty_pattern():
    s, p = "a", ""
    solver = Solution()
    assert solver.isMatch(s, p) == False, "Failed on empty pattern"

def test_empty_string():
    s, p = "", "a*"
    solver = Solution()
    assert solver.isMatch(s, p) == True, "Failed on empty string with pattern"
"""
