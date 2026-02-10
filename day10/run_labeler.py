#!/usr/bin/env python3
import sys
import os

# Add current directory to path so we can resolve labeler_app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from labeler_app.main import main

if __name__ == "__main__":
    main()
