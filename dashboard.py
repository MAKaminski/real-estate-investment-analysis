#!/usr/bin/env python3
"""
Real Estate Investment Analysis Tool - Dashboard Entry Point
==========================================================

This is the entry point for launching the web dashboard.
It imports and runs the dashboard from the src directory.
"""

import sys
import os

# Add the current directory to the path so we can import from src
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the dashboard
from src.dashboard import app

if __name__ == "__main__":
    print("Starting Real Estate Investment Analysis Dashboard...")
    print("Open your browser and go to: http://127.0.0.1:8050")
    app.run(debug=True, host='0.0.0.0', port=8050)
