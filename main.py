"""
Sudoku Game Entry Point
Runs the Sudoku CLI application.
"""

import sys
import os

# Ensure project root directory is in Python module search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.cli_ui import CLIInterface

def main():
    game_ui = CLIInterface()
    game_ui.start_game()

if __name__ == "__main__":
    main()
