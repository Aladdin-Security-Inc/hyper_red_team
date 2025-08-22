# problems/valid_palindrome.py

problem_description = """
Given a string `s`, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.

An empty string is considered a valid palindrome.

Example 1:
Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.

Example 2:
Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
"""

test_code = """
import pytest
from solution import Solution

def test_example_1():
    s = "A man, a plan, a canal: Panama"
    solver = Solution()
    assert solver.isPalindrome(s) == True, "Failed on example 1"

def test_example_2():
    s = "race a car"
    solver = Solution()
    assert solver.isPalindrome(s) == False, "Failed on example 2"

def test_empty_string():
    s = ""
    solver = Solution()
    assert solver.isPalindrome(s) == True, "Failed on empty string"

def test_non_alphanumeric():
    s = ".,,,"
    solver = Solution()
    assert solver.isPalindrome(s) == True, "Failed on only non-alphanumeric characters"

def test_single_char():
    s = "a"
    solver = Solution()
    assert solver.isPalindrome(s) == True, "Failed on single character"

def test_mixed_case():
    s = "No lemon, no melon"
    solver = Solution()
    assert solver.isPalindrome(s) == True, "Failed on mixed case palindrome"
"""
