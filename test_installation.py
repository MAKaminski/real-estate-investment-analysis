#!/usr/bin/env python3
"""
Real Estate Investment Analysis Tool - Test Entry Point
=====================================================

This is the entry point for running the installation tests.
It imports and runs the tests from the src directory.
"""

import sys
import os

# Add the current directory to the path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the tests
from src.test_installation import main

if __name__ == "__main__":
    sys.exit(main())
