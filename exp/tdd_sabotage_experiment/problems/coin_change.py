# problems/coin_change.py

problem_description = """
You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.

Example 1:
Input: coins = [1, 2, 5], amount = 11
Output: 3
Explanation: 11 = 5 + 5 + 1

Example 2:
Input: coins = [2], amount = 3
Output: -1

Example 3:
Input: coins = [1], amount = 0
Output: 0
"""

test_code = """
import pytest
from solution import Solution

def test_example_1():
    coins = [1, 2, 5]
    amount = 11
    solver = Solution()
    assert solver.coinChange(coins, amount) == 3, "Failed on example 1"

def test_example_2():
    coins = [2]
    amount = 3
    solver = Solution()
    assert solver.coinChange(coins, amount) == -1, "Failed on example 2"

def test_amount_is_zero():
    coins = [1]
    amount = 0
    solver = Solution()
    assert solver.coinChange(coins, amount) == 0, "Failed when amount is 0"

def test_no_solution():
    coins = [2, 5]
    amount = 3
    solver = Solution()
    assert solver.coinChange(coins, amount) == -1, "Failed on a case with no solution"

def test_large_amount():
    coins = [1, 5, 10, 25]
    amount = 100
    solver = Solution()
    assert solver.coinChange(coins, amount) == 4, "Failed on a larger amount"

def test_single_coin_type():
    coins = [7]
    amount = 21
    solver = Solution()
    assert solver.coinChange(coins, amount) == 3, "Failed on a single coin type"
"""
