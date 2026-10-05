"""
Sudoku Rule Validator
Validates numbers against standard Sudoku constraints.
"""

class SudokuValidator:
    @staticmethod
    def is_valid_row(grid, row: int, num: int, current_col: int = -1) -> bool:
        for c in range(9):
            if c != current_col and grid[row][c] == num:
                return False
        return True

    @staticmethod
    def is_valid_col(grid, col: int, num: int, current_row: int = -1) -> bool:
        for r in range(9):
            if r != current_row and grid[r][col] == num:
                return False
        return True

    @staticmethod
    def is_valid_box(grid, row: int, col: int, num: int, current_pos=None) -> bool:
        box_start_row = 3 * (row // 3)
        box_start_col = 3 * (col // 3)
        for r in range(3):
            for c in range(3):
                r_idx = box_start_row + r
                c_idx = box_start_col + c
                if current_pos and (r_idx, c_idx) == current_pos:
                    continue
                if grid[r_idx][c_idx] == num:
                    return False
        return True

    @classmethod
    def is_valid_move(cls, grid, row: int, col: int, num: int) -> bool:
        if num < 1 or num > 9:
            return False
        return (cls.is_valid_row(grid, row, num, col) and
                cls.is_valid_col(grid, col, num, row) and
                cls.is_valid_box(grid, row, col, num, (row, col)))
