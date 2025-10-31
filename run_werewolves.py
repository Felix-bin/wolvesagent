#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Entry point for running the werewolf game."""
import asyncio
import sys
import os

# Add the current directory to Python path to ensure proper imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from werewolves.main import main

if __name__ == "__main__":
    asyncio.run(main())
