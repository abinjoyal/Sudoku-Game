"""
Sudoku CLI User Interface
Handles formatted terminal grid rendering and user interaction loop.
"""

from src.core.board import SudokuBoard
from src.core.validator import SudokuValidator
from src.core.solver import SudokuSolver
from src.generator.puzzle_generator import PuzzleGenerator

class CLIInterface:
    def __init__(self):
        self.board = None

    def display_board(self):
        if not self.board:
            return

        print("\n" + "=" * 37)
        print("            S U D O K U            ")
        print("=" * 37)
        print("     1 2 3   4 5 6   7 8 9 (Cols)")
        print("   +-------+-------+-------+")

        for r in range(9):
            row_str = f" {r + 1} | "
            for c in range(9):
                val = self.board.get_val(r, c)
                display_char = "." if val == 0 else str(val)
                row_str += f"{display_char} "

                if (c + 1) % 3 == 0:
                    row_str += "| "
            print(row_str)

            if (r + 1) % 3 == 0:
                print("   +-------+-------+-------+")
        print(" (Rows)\n")

    def start_game(self):
        print("\nWelcome to Professional Python Sudoku!")
        print("Select Difficulty: [1] Easy  [2] Medium  [3] Hard")

        choice = input("Enter choice (1-3) [Default 2]: ").strip()
        difficulty_map = {"1": "easy", "2": "medium", "3": "hard"}
        diff = difficulty_map.get(choice, "medium")

        print(f"\nGenerating {diff.upper()} puzzle...")
        puzzle_grid = PuzzleGenerator.generate_puzzle(diff)
        self.board = SudokuBoard(puzzle_grid)

        while True:
            self.display_board()

            if self.board.is_complete():
                print("🎉 CONGRATULATIONS! You solved the Sudoku puzzle! 🎉")
                break

            print("Commands: 'set <row> <col> <val>' | 'solve' | 'quit'")
            cmd = input("Enter move (e.g. set 1 5 3): ").strip().lower()

            if cmd == 'quit':
                print("Thanks for playing!")
                break
            elif cmd == 'solve':
                print("\nSolving puzzle using Backtracking Solver...")
                solving_grid = [row[:] for row in self.board.grid]
                if SudokuSolver.solve(solving_grid):
                    self.board.grid = solving_grid
                    self.display_board()
                    print("✅ Puzzle Solved automatically!")
                else:
                    print("❌ No valid solution exists for the current board state.")
                break
            elif cmd.startswith('set'):
                parts = cmd.split()
                if len(parts) == 4:
                    try:
                        r = int(parts[1]) - 1
                        c = int(parts[2]) - 1
                        v = int(parts[3])

                        if 0 <= r < 9 and 0 <= c < 9 and 1 <= v <= 9:
                            if self.board.is_original(r, c):
                                print("⚠️ Cannot change pre-filled original puzzle numbers!")
                            elif not SudokuValidator.is_valid_move(self.board.grid, r, c, v):
                                print(f"⚠️ Invalid move! {v} conflicts with row, column, or 3x3 box.")
                            else:
                                self.board.set_val(r, c, v)
                                print(f"✓ Placed {v} at Row {r+1}, Col {c+1}")
                        else:
                            print("⚠️ Row/Col must be 1-9 and Value must be 1-9.")
                    except ValueError:
                        print("⚠️ Invalid format! Example: set 1 5 3")
                else:
                    print("⚠️ Invalid format! Example: set 1 5 3")
            else:
                print("⚠️ Unknown command! Use 'set <r> <c> <v>', 'solve', or 'quit'.")
