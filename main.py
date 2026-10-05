"""
Sudoku Game Entry Point
Launches the Graphical User Interface (GUI) Desktop Window.
"""

import sys
import os
import tkinter as tk

# Ensure project root directory is in Python module search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.ui.gui_ui import SudokuGUI

def main():
    root = tk.Tk()
    app = SudokuGUI(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass  # Gracefully exit on Ctrl+C without showing traceback

if __name__ == "__main__":
    main()
