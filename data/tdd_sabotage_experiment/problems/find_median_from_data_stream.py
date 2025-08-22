# problems/find_median_from_data_stream.py

problem_description = """
The median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

For example, for arr = [2,3,4], the median is 3.
For example, for arr = [2,3], the median is (2 + 3) / 2 = 2.5.

Implement the MedianFinder class:
- `MedianFinder()` initializes the MedianFinder object.
- `void addNum(int num)` adds the integer num from the data stream to the data structure.
- `double findMedian()` returns the median of all elements so far.

Example:
Input
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
Output
[null, null, null, 1.5, null, 2.0]

Explanation
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
medianFinder.addNum(3);    // arr = [1, 2, 3]
medianFinder.findMedian(); // return 2.0
"""

test_code = """
import pytest
from solution import MedianFinder

def test_sequence_of_operations():
    mf = MedianFinder()
    mf.addNum(1)
    mf.addNum(2)
    assert mf.findMedian() == 1.5, "Failed after adding 1, 2"
    mf.addNum(3)
    assert mf.findMedian() == 2.0, "Failed after adding 3"

def test_negative_numbers():
    mf = MedianFinder()
    mf.addNum(-1)
    assert mf.findMedian() == -1.0
    mf.addNum(-2)
    assert mf.findMedian() == -1.5
    mf.addNum(-3)
    assert mf.findMedian() == -2.0

def test_zeros():
    mf = MedianFinder()
    mf.addNum(0)
    assert mf.findMedian() == 0.0
    mf.addNum(0)
    assert mf.findMedian() == 0.0

def test_mixed_order():
    mf = MedianFinder()
    mf.addNum(6)
    assert mf.findMedian() == 6.0
    mf.addNum(10)
    assert mf.findMedian() == 8.0
    mf.addNum(2)
    assert mf.findMedian() == 6.0
    mf.addNum(6)
    assert mf.findMedian() == 6.0
    mf.addNum(5)
    assert mf.findMedian() == 6.0
    mf.addNum(0)
    assert mf.findMedian() == 5.5
"""
