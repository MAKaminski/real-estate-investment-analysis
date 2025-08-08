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
    import socket
    
    def find_free_port(start_port=8050):
        """Find a free port starting from start_port"""
        port = start_port
        while port < start_port + 100:  # Try up to 100 ports
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                port += 1
        return None
    
    print("Starting Real Estate Investment Analysis Dashboard...")
    
    # Find a free port
    port = find_free_port(8050)
    if port is None:
        print("Error: No free ports available in range 8050-8149")
        sys.exit(1)
    
    print(f"Open your browser and go to: http://127.0.0.1:{port}")
    try:
        app.run(debug=True, host='0.0.0.0', port=port)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"Port {port} is in use. Trying alternative port...")
            alt_port = find_free_port(port + 1)
            if alt_port:
                print(f"Using alternative port: {alt_port}")
                print(f"Open your browser and go to: http://127.0.0.1:{alt_port}")
                app.run(debug=True, host='0.0.0.0', port=alt_port)
            else:
                print("Error: No free ports available")
                sys.exit(1)
        else:
            raise e
