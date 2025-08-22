# problems/n_queens.py

problem_description = """
The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.

Given an integer `n`, return all distinct solutions to the n-queens puzzle. You may return the answer in any order.

Each solution contains a distinct board configuration of the n-queens' placement, where `'Q'` and `'.'` both indicate a queen and an empty space, respectively.

Example 1:
Input: n = 4
Output: [
    [".Q..","...Q","Q...","..Q."],
    ["..Q.","Q...","...Q",".Q.."]
]

Example 2:
Input: n = 1
Output: [["Q"]]
"""

test_code = """
import pytest
from solution import Solution

def sort_solutions(solutions):
    # Sort each board representation and then the list of boards
    # to ensure a canonical order for comparison.
    return sorted([sorted(board) for board in solutions])

def test_n_equals_4():
    n = 4
    expected = [
        [".Q..", "...Q", "Q...", "..Q."],
        ["..Q.", "Q...", "...Q", ".Q.."]
    ]
    solver = Solution()
    result = solver.solveNQueens(n)
    assert sort_solutions(result) == sort_solutions(expected), "Failed on n=4"
    assert len(result) == 2, "Incorrect number of solutions for n=4"

def test_n_equals_1():
    n = 1
    expected = [["Q"]]
    solver = Solution()
    result = solver.solveNQueens(n)
    assert sort_solutions(result) == sort_solutions(expected), "Failed on n=1"
    assert len(result) == 1, "Incorrect number of solutions for n=1"

def test_n_equals_2():
    n = 2
    expected = []
    solver = Solution()
    result = solver.solveNQueens(n)
    assert len(result) == 0, "Failed on n=2, which has no solutions"

def test_n_equals_3():
    n = 3
    expected = []
    solver = Solution()
    result = solver.solveNQueens(n)
    assert len(result) == 0, "Failed on n=3, which has no solutions"
"""
