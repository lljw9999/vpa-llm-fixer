#!/usr/bin/env python3
"""
VPA package entry point - enables 'python -m vpa' usage.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import and run main
from main import main

if __name__ == "__main__":
    main()
