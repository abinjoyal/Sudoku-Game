"""
Sudoku Board Data Model
Manages 9x9 grid state and cell mutations.
"""

class SudokuBoard:
    def __init__(self, initial_grid=None):
        if initial_grid:
            self.grid = [row[:] for row in initial_grid]
            self.original_grid = [row[:] for row in initial_grid]
        else:
            self.grid = [[0 for _ in range(9)] for _ in range(9)]
            self.original_grid = [[0 for _ in range(9)] for _ in range(9)]

    def get_val(self, row: int, col: int) -> int:
        return self.grid[row][col]

    def set_val(self, row: int, col: int, val: int) -> bool:
        if self.is_original(row, col):
            return False
        self.grid[row][col] = val
        return True

    def clear_val(self, row: int, col: int) -> bool:
        if self.is_original(row, col):
            return False
        self.grid[row][col] = 0
        return True

    def is_original(self, row: int, col: int) -> bool:
        return self.original_grid[row][col] != 0

    def is_complete(self) -> bool:
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return False
        return True

    def copy(self):
        new_board = SudokuBoard(self.grid)
        new_board.original_grid = [row[:] for row in self.original_grid]
        return new_board
