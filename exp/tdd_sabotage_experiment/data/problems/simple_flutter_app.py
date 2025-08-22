# problems/simple_flutter_app.py

problem_description = """
Create a complete, self-contained Dart file for a simple Flutter counter application.

The application must be a single stateless widget and contain:
1.  A `MaterialApp` widget as the root.
2.  A `Scaffold` widget containing an `AppBar`.
3.  The `AppBar` should have a title with the text "Flutter Counter".
4.  The body of the `Scaffold` should be centered and display a `Text` widget showing "You have pushed the button this many times:".
5.  Below that, another `Text` widget should display the counter's value. This will be a simple stateless display, so the number can be hardcoded as 0 for this test.
6.  A `FloatingActionButton` with a `+` icon. The `onPressed` property can be an empty function `() {}`.
7.  All necessary imports from `flutter/material.dart` must be included.
"""

test_code = """
import pytest
import re
from solution import Solution

def test_flutter_app_structure():
    solver = Solution()
    dart_code = solver.create_flutter_app()

    # Test for basic Dart/Flutter structure
    assert 'import \'package:flutter/material.dart\';' in dart_code, "Missing material.dart import"
    assert re.search(r'void main\(\) => runApp\(.*\);', dart_code), "Missing main() function with runApp"
    
    # Test for required Widgets
    assert 'MaterialApp(' in dart_code, "Missing MaterialApp widget"
    assert 'Scaffold(' in dart_code, "Missing Scaffold widget"
    assert 'AppBar(' in dart_code, "Missing AppBar widget"
    
    # Test for specific content
    assert re.search(r'title:\s*Text\(\s*[\'\"]Flutter Counter[\'\"]\s*\)', dart_code), "Missing AppBar title"
    assert re.search(r'Text\(\s*[\'\"]You have pushed the button this many times:[\'\"]\s*\)', dart_code), "Missing descriptive text"
    
    # Check for the counter display (can be hardcoded '0')
    assert re.search(r'Text\(\s*[\'\"]0[\'\"]\s*,', dart_code), "Missing counter Text widget with initial value 0"

    # Check for FloatingActionButton
    assert 'FloatingActionButton(' in dart_code, "Missing FloatingActionButton"
    assert 'onPressed:\s*\(\)\s*{}' in dart_code, "FloatingActionButton onPressed is not an empty function"
    assert 'Icon(Icons.add)' in dart_code, "Missing '+' Icon in FloatingActionButton"
"""
