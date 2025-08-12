# problems/simple_counter_app.py

problem_description = """
Create a complete, self-contained HTML file for a simple counter application.

The application must have:
1.  A heading (h1) with the text "Simple Counter".
2.  A display area (e.g., a `div` or `span`) with an `id` of "counter". It should initially display the number 0.
3.  An increment button with an `id` of "increment". When clicked, it should increase the counter's value by 1.
4.  A decrement button with an `id` of "decrement". When clicked, it should decrease the counter's value by 1.
5.  All necessary JavaScript logic must be included within a `<script>` tag in the same HTML file. The JavaScript should handle the button clicks and update the display.
6.  Add some basic CSS to center the elements and make the buttons look presentable.
"""

test_code = """
import pytest
import re
from solution import Solution

def test_html_structure_and_content():
    solver = Solution()
    html_content = solver.create_counter_app()

    # Test for basic HTML structure
    assert re.search(r'<!DOCTYPE html>', html_content, re.IGNORECASE), "Missing DOCTYPE"
    assert re.search(r'<html.*>', html_content, re.IGNORECASE), "Missing <html> tag"
    assert re.search(r'<head.*>', html_content, re.IGNORECASE), "Missing <head> tag"
    assert re.search(r'<body.*>', html_content, re.IGNORECASE), "Missing <body> tag"
    assert re.search(r'<style.*>', html_content, re.IGNORECASE | re.DOTALL), "Missing <style> tag for CSS"

    # Test for required elements
    assert re.search(r'<h1>\s*Simple Counter\s*</h1>', html_content, re.IGNORECASE), "Missing h1 heading"
    
    # Check for the counter display, allowing for flexible tags (div or span)
    counter_match = re.search(r'<(div|span)\s+id="counter"[^>]*>\s*0\s*</\1>', html_content)
    assert counter_match, "Missing counter display area with initial value 0"

    # Check for buttons
    assert re.search(r'<button\s+id="increment"[^>]*>.*?</button>', html_content, re.IGNORECASE), "Missing increment button"
    assert re.search(r'<button\s+id="decrement"[^>]*>.*?</button>', html_content, re.IGNORECASE), "Missing decrement button"

    # Test for JavaScript logic
    script_content_match = re.search(r'<script.*>(.*)</script>', html_content, re.IGNORECASE | re.DOTALL)
    assert script_content_match, "Missing <script> tag for JavaScript"
    
    script_content = script_content_match.group(1)
    assert 'getElementById("counter")' in script_content, "JS does not reference the counter element"
    assert 'getElementById("increment")' in script_content, "JS does not reference the increment button"
    assert 'getElementById("decrement")' in script_content, "JS does not reference the decrement button"
    assert 'addEventListener("click"' in script_content, "JS is missing click event listeners"
"""
