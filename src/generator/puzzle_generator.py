"""
Sudoku Puzzle Generator
Generates valid solvable Sudoku puzzles with varying difficulty levels.
"""

import random
from src.core.solver import SudokuSolver
from src.core.validator import SudokuValidator

class PuzzleGenerator:
    @staticmethod
    def generate_full_board():
        grid = [[0 for _ in range(9)] for _ in range(9)]
        PuzzleGenerator._fill_board(grid)
        return grid

    @staticmethod
    def _fill_board(grid):
        empty = SudokuSolver.find_empty_cell(grid)
        if not empty:
            return True

        row, col = empty
        numbers = list(range(1, 10))
        random.shuffle(numbers)

        for num in numbers:
            if SudokuValidator.is_valid_move(grid, row, col, num):
                grid[row][col] = num
                if PuzzleGenerator._fill_board(grid):
                    return True
                grid[row][col] = 0
        return False

    @staticmethod
    def generate_puzzle(difficulty: str = "medium"):
        full_grid = PuzzleGenerator.generate_full_board()
        puzzle_grid = [row[:] for row in full_grid]

        difficulty_remove_count = {
            "easy": 30,
            "medium": 42,
            "hard": 52
        }
        remove_count = difficulty_remove_count.get(difficulty.lower(), 42)

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)

        removed = 0
        for r, c in cells:
            if removed >= remove_count:
                break
            puzzle_grid[r][c] = 0
            removed += 1

        return puzzle_grid
