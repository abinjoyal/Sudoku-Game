"""
Sudoku Backtracking Solver
Solves Sudoku grids using depth-first search with backtracking.
"""

from src.core.validator import SudokuValidator

class SudokuSolver:
    @staticmethod
    def find_empty_cell(grid):
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    return r, c
        return None

    @classmethod
    def solve(cls, grid) -> bool:
        empty = cls.find_empty_cell(grid)
        if not empty:
            return True  # Puzzle solved!

        row, col = empty

        for num in range(1, 10):
            if SudokuValidator.is_valid_move(grid, row, col, num):
                grid[row][col] = num

                if cls.solve(grid):
                    return True

                grid[row][col] = 0  # Backtrack

        return False
