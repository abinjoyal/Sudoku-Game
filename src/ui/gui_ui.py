"""
Sudoku Graphical User Interface (GUI)
Built with Python Tkinter framework.
Clean visual grid with validation and solver integration.
Avoids emojis as per configuration directive.
"""

import sys
import tkinter as tk
from tkinter import messagebox, ttk

from src.core.board import SudokuBoard
from src.core.validator import SudokuValidator
from src.core.solver import SudokuSolver
from src.generator.puzzle_generator import PuzzleGenerator


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game & Solver")
        self.root.geometry("540x640")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.board = None
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.difficulty_var = tk.StringVar(value="medium")

        self._setup_styles()
        self._create_widgets()
        self.new_game()

    def _on_closing(self):
        self.root.quit()
        self.root.destroy()


    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

    def _create_widgets(self):
        # Top Header & Controls
        control_frame = tk.Frame(self.root, bg="#F0F0F0", padx=10, pady=10)
        control_frame.pack(fill=tk.X, side=tk.TOP)

        tk.Label(
            control_frame,
            text="Difficulty:",
            font=("Segoe UI", 10, "bold"),
            bg="#F0F0F0"
        ).pack(side=tk.LEFT, padx=(5, 5))

        diff_combo = ttk.Combobox(
            control_frame,
            textvariable=self.difficulty_var,
            values=["easy", "medium", "hard"],
            state="readonly",
            width=10,
            font=("Segoe UI", 10)
        )
        diff_combo.pack(side=tk.LEFT, padx=(0, 15))

        btn_new = tk.Button(
            control_frame,
            text="New Game",
            command=self.new_game,
            font=("Segoe UI", 9, "bold"),
            bg="#2B579A",
            fg="white",
            activebackground="#1E3D6B",
            activeforeground="white",
            padx=10,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_new.pack(side=tk.LEFT, padx=4)

        btn_solve = tk.Button(
            control_frame,
            text="Solve Puzzle",
            command=self.solve_puzzle,
            font=("Segoe UI", 9, "bold"),
            bg="#27AE60",
            fg="white",
            activebackground="#1E8449",
            activeforeground="white",
            padx=10,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_solve.pack(side=tk.LEFT, padx=4)

        btn_reset = tk.Button(
            control_frame,
            text="Reset",
            command=self.reset_board,
            font=("Segoe UI", 9, "bold"),
            bg="#E74C3C",
            fg="white",
            activebackground="#C0392B",
            activeforeground="white",
            padx=10,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_reset.pack(side=tk.LEFT, padx=4)

        # Main 9x9 Board Frame
        board_container = tk.Frame(self.root, bg="#222222", bd=2)
        board_container.pack(expand=True, fill=tk.BOTH, padx=15, pady=15)

        # 3x3 Sub-grid blocks
        for block_row in range(3):
            for block_col in range(3):
                block_frame = tk.Frame(
                    board_container,
                    bd=1.5,
                    relief=tk.SOLID,
                    bg="#222222"
                )
                block_frame.grid(
                    row=block_row,
                    column=block_col,
                    padx=1.5,
                    pady=1.5,
                    sticky="nsew"
                )

                for r in range(3):
                    for c in range(3):
                        row = block_row * 3 + r
                        col = block_col * 3 + c

                        entry = tk.Entry(
                            block_frame,
                            width=2,
                            font=("Segoe UI", 16, "bold"),
                            justify="center",
                            bd=1,
                            relief=tk.FLAT
                        )
                        entry.grid(
                            row=r,
                            column=c,
                            padx=1,
                            pady=1,
                            ipady=6,
                            sticky="nsew"
                        )

                        # Validation callback on key input
                        vcmd = (self.root.register(self._validate_input), "%P", str(row), str(col))
                        entry.config(validate="key", validatecommand=vcmd)

                        self.entries[row][col] = entry

                for i in range(3):
                    block_frame.grid_rowconfigure(i, weight=1)
                    block_frame.grid_columnconfigure(i, weight=1)

        for i in range(3):
            board_container.grid_rowconfigure(i, weight=1)
            board_container.grid_columnconfigure(i, weight=1)

        # Status Bar
        self.status_label = tk.Label(
            self.root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Segoe UI", 9),
            bg="#F9F9F9",
            padx=10,
            pady=4
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def _validate_input(self, new_val, row_str, col_str):
        row, col = int(row_str), int(col_str)

        if new_val == "":
            if self.board and not self.board.is_original(row, col):
                self.board.set_val(row, col, 0)
            return True

        if len(new_val) > 1 or not new_val.isdigit():
            return False

        val = int(new_val)
        if val == 0:
            return False

        if self.board:
            if self.board.is_original(row, col):
                return False

            if not SudokuValidator.is_valid_move(self.board.grid, row, col, val):
                self.status_label.config(
                    text=f"Invalid move: Number {val} conflicts at Row {row+1}, Col {col+1}.",
                    fg="red"
                )
                return True
            else:
                self.board.set_val(row, col, val)
                self.status_label.config(
                    text=f"Placed {val} at Row {row+1}, Col {col+1}.",
                    fg="green"
                )

                if self.board.is_complete():
                    messagebox.showinfo("Success", "Congratulations! You solved the Sudoku puzzle!")
                    self.status_label.config(text="Puzzle Completed Successfully!", fg="green")

        return True

    def new_game(self):
        diff = self.difficulty_var.get().lower()
        puzzle_grid = PuzzleGenerator.generate_puzzle(diff)
        self.board = SudokuBoard(puzzle_grid)
        self._update_gui_from_board()
        self.status_label.config(
            text=f"New Game Started. Difficulty: {diff.capitalize()}",
            fg="black"
        )

    def reset_board(self):
        if not self.board:
            return
        for r in range(9):
            for c in range(9):
                if not self.board.is_original(r, c):
                    self.board.set_val(r, c, 0)
        self._update_gui_from_board()
        self.status_label.config(text="Board reset to initial state.", fg="black")

    def solve_puzzle(self):
        if not self.board:
            return

        grid_to_solve = [row[:] for row in self.board.grid]
        if SudokuSolver.solve(grid_to_solve):
            self.board.grid = grid_to_solve
            self._update_gui_from_board(solving=True)
            self.status_label.config(text="Puzzle solved successfully by Backtracking AI.", fg="green")
            messagebox.showinfo("Solved", "Puzzle solved successfully!")
        else:
            messagebox.showerror("Error", "No valid solution exists for the current board configuration.")
            self.status_label.config(text="Error: No solution exists.", fg="red")

    def _update_gui_from_board(self, solving=False):
        for r in range(9):
            for c in range(9):
                entry = self.entries[r][c]
                val = self.board.get_val(r, c)

                entry.config(validate="none")
                entry.delete(0, tk.END)

                if val != 0:
                    entry.insert(0, str(val))

                if self.board.is_original(r, c):
                    entry.config(
                        bg="#E0E0E0",
                        fg="#111111",
                        state="disabled",
                        disabledbackground="#E0E0E0",
                        disabledforeground="#111111"
                    )
                else:
                    if solving:
                        entry.config(
                            bg="#E8F8F5",
                            fg="#27AE60",
                            state="normal"
                        )
                    else:
                        entry.config(
                            bg="#FFFFFF",
                            fg="#0055FF",
                            state="normal"
                        )

                entry.config(validate="key")
