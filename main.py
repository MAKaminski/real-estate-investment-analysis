#!/usr/bin/env python3
"""
Real Estate Investment Analysis Tool - Main Entry Point
======================================================

This is the main entry point for the real estate investment analysis tool.
It imports and runs the main application from the src directory.
"""

import sys
import os

# Add the current directory to the path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main application
from src.main import main

if __name__ == "__main__":
    sys.exit(main())
