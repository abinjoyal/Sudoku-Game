"""
Sudoku Graphical User Interface (GUI)
Built with Python Tkinter framework.
Features: 9x9 grid, Backtracking AI Solver, Dynamic Timer,
Real-time Red/Green Validation, Hint System, Best Time Persistence,
Undo/Redo History, and Same-Number Highlight Guide.
Avoids emojis as per configuration directive.
"""

import json
import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from src.core.board import SudokuBoard
from src.core.validator import SudokuValidator
from src.core.solver import SudokuSolver
from src.generator.puzzle_generator import PuzzleGenerator


class SudokuGUI:
    SCORES_FILE = os.path.join("data", "high_scores.json")

    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game & Solver")
        self.root.geometry("680x540")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        self.board = None
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.cell_states = [[{"bg": "#FFFFFF", "fg": "#0055FF"} for _ in range(9)] for _ in range(9)]
        self.difficulty_var = tk.StringVar(value="medium")

        # Move History Stacks for Undo / Redo
        self.history = []
        self.redo_stack = []

        # Timer State Variables
        self.timer_seconds = 0
        self.timer_running = False
        self.timer_job = None

        # High Scores Storage
        self.high_scores = self._load_high_scores()

        self._setup_styles()
        self._create_widgets()
        self._bind_shortcuts()
        self.new_game()

    def _on_closing(self):
        self._stop_timer()
        self.root.quit()
        self.root.destroy()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

    def _bind_shortcuts(self):
        self.root.bind("<Control-z>", lambda e: self.undo_move())
        self.root.bind("<Control-y>", lambda e: self.redo_move())

    def _load_high_scores(self):
        if os.path.exists(self.SCORES_FILE):
            try:
                with open(self.SCORES_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"easy": None, "medium": None, "hard": None}

    def _save_high_scores(self):
        try:
            folder = os.path.dirname(self.SCORES_FILE)
            if folder:
                os.makedirs(folder, exist_ok=True)
            with open(self.SCORES_FILE, "w") as f:
                json.dump(self.high_scores, f, indent=2)
        except Exception:
            pass

    def _format_seconds(self, seconds):
        if seconds is None:
            return "--:--"
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def _create_widgets(self):
        # Top Header & Controls
        control_frame = tk.Frame(self.root, bg="#F0F0F0", padx=8, pady=10)
        control_frame.pack(fill=tk.X, side=tk.TOP)

        tk.Label(
            control_frame,
            text="Diff:",
            font=("Segoe UI", 9, "bold"),
            bg="#F0F0F0"
        ).pack(side=tk.LEFT, padx=(2, 2))

        diff_combo = ttk.Combobox(
            control_frame,
            textvariable=self.difficulty_var,
            values=["easy", "medium", "hard"],
            state="readonly",
            width=7,
            font=("Segoe UI", 9)
        )
        diff_combo.pack(side=tk.LEFT, padx=(0, 6))
        diff_combo.bind("<<ComboboxSelected>>", self._on_difficulty_changed)

        btn_new = tk.Button(
            control_frame,
            text="New Game",
            command=self.new_game,
            font=("Segoe UI", 9, "bold"),
            bg="#2B579A",
            fg="white",
            activebackground="#1E3D6B",
            activeforeground="white",
            padx=5,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_new.pack(side=tk.LEFT, padx=2)

        btn_undo = tk.Button(
            control_frame,
            text="Undo",
            command=self.undo_move,
            font=("Segoe UI", 9, "bold"),
            bg="#34495E",
            fg="white",
            activebackground="#2C3E50",
            activeforeground="white",
            padx=5,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_undo.pack(side=tk.LEFT, padx=2)

        btn_redo = tk.Button(
            control_frame,
            text="Redo",
            command=self.redo_move,
            font=("Segoe UI", 9, "bold"),
            bg="#7F8C8D",
            fg="white",
            activebackground="#707B7C",
            activeforeground="white",
            padx=5,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_redo.pack(side=tk.LEFT, padx=2)

        btn_hint = tk.Button(
            control_frame,
            text="Get Hint",
            command=self.get_hint,
            font=("Segoe UI", 9, "bold"),
            bg="#8E44AD",
            fg="white",
            activebackground="#6C3483",
            activeforeground="white",
            padx=5,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_hint.pack(side=tk.LEFT, padx=2)

        btn_solve = tk.Button(
            control_frame,
            text="Solve Puzzle",
            command=self.solve_puzzle,
            font=("Segoe UI", 9, "bold"),
            bg="#27AE60",
            fg="white",
            activebackground="#1E8449",
            activeforeground="white",
            padx=5,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_solve.pack(side=tk.LEFT, padx=2)

        btn_reset = tk.Button(
            control_frame,
            text="Reset",
            command=self.reset_board,
            font=("Segoe UI", 9, "bold"),
            bg="#E74C3C",
            fg="white",
            activebackground="#C0392B",
            activeforeground="white",
            padx=5,
            pady=4,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_reset.pack(side=tk.LEFT, padx=2)

        # High Score / Best Time Label
        self.best_label = tk.Label(
            control_frame,
            text="Best: --:--",
            font=("Segoe UI", 9, "bold"),
            bg="#F0F0F0",
            fg="#8E44AD"
        )
        self.best_label.pack(side=tk.RIGHT, padx=(2, 4))

        # Timer Display Label
        self.timer_label = tk.Label(
            control_frame,
            text="Time: 00:00",
            font=("Segoe UI", 9, "bold"),
            bg="#F0F0F0",
            fg="#2C3E50"
        )
        self.timer_label.pack(side=tk.RIGHT, padx=(2, 2))

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

                        # Same Number Focus Highlight bindings
                        entry.bind("<FocusIn>", lambda e, row_idx=row, col_idx=col: self._on_cell_focus(row_idx, col_idx))
                        entry.bind("<KeyRelease>", lambda e, row_idx=row, col_idx=col: self._on_cell_focus(row_idx, col_idx))

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

    def _on_difficulty_changed(self, event=None):
        diff = self.difficulty_var.get().lower()
        best_sec = self.high_scores.get(diff)
        self.best_label.config(text=f"Best: {self._format_seconds(best_sec)}")

    def _on_cell_focus(self, row, col):
        if not self.board:
            return
        target_val = self.board.get_val(row, col)

        for r in range(9):
            for c in range(9):
                entry = self.entries[r][c]
                val = self.board.get_val(r, c)
                state = self.cell_states[r][c]

                if target_val != 0 and val == target_val:
                    # Soft Cyan highlight for matching numbers
                    if self.board.is_original(r, c):
                        entry.config(bg="#BBDEFB")
                    else:
                        entry.config(bg="#E1F5FE")
                else:
                    # Restore base state background
                    entry.config(bg=state["bg"])

    # Timer Methods
    def _start_timer(self):
        self._stop_timer()
        self.timer_seconds = 0
        self.timer_running = True
        self._tick_timer()

    def _stop_timer(self):
        self.timer_running = False
        if self.timer_job:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def _tick_timer(self):
        if self.timer_running:
            mins = self.timer_seconds // 60
            secs = self.timer_seconds % 60
            self.timer_label.config(text=f"Time: {mins:02d}:{secs:02d}")
            self.timer_seconds += 1
            self.timer_job = self.root.after(1000, self._tick_timer)

    def _get_formatted_time(self):
        elapsed = self.timer_seconds - 1 if self.timer_seconds > 0 else 0
        mins = elapsed // 60
        secs = elapsed % 60
        return f"{mins:02d}:{secs:02d}"

    def _validate_input(self, new_val, row_str, col_str):
        row, col = int(row_str), int(col_str)
        entry = self.entries[row][col]

        if new_val == "":
            if self.board and not self.board.is_original(row, col):
                old_val = self.board.get_val(row, col)
                if old_val != 0:
                    self.history.append((row, col, old_val, 0))
                    self.redo_stack.clear()

                self.board.set_val(row, col, 0)
                self.cell_states[row][col] = {"bg": "#FFFFFF", "fg": "#0055FF"}
                if entry:
                    entry.config(bg="#FFFFFF", fg="#0055FF")
            return True

        if len(new_val) > 1 or not new_val.isdigit():
            return False

        val = int(new_val)
        if val == 0:
            return False

        if self.board:
            if self.board.is_original(row, col):
                return False

            old_val = self.board.get_val(row, col)
            if old_val != val:
                self.history.append((row, col, old_val, val))
                self.redo_stack.clear()

            if not SudokuValidator.is_valid_move(self.board.grid, row, col, val):
                # Invalid / Wrong Move: Red Highlight
                self.cell_states[row][col] = {"bg": "#FFEBEE", "fg": "#D32F2F"}
                if entry:
                    entry.config(bg="#FFEBEE", fg="#D32F2F")
                self.board.set_val(row, col, val)
                self.status_label.config(
                    text=f"Invalid move: Number {val} conflicts at Row {row+1}, Col {col+1}.",
                    fg="red"
                )
                return True
            else:
                # Valid / Correct Move: Green Highlight
                self.cell_states[row][col] = {"bg": "#E8F5E9", "fg": "#2E7D32"}
                if entry:
                    entry.config(bg="#E8F5E9", fg="#2E7D32")
                self.board.set_val(row, col, val)
                self.status_label.config(
                    text=f"Placed {val} at Row {row+1}, Col {col+1}.",
                    fg="green"
                )

                if self.board.is_complete():
                    self._handle_victory()

        return True

    def undo_move(self):
        if not self.history or not self.board:
            self.status_label.config(text="Undo: No moves to undo.", fg="black")
            return

        row, col, old_val, new_val = self.history.pop()
        self.redo_stack.append((row, col, old_val, new_val))

        self.board.set_val(row, col, old_val)
        entry = self.entries[row][col]

        entry.config(validate="none")
        entry.delete(0, tk.END)

        if old_val == 0:
            self.cell_states[row][col] = {"bg": "#FFFFFF", "fg": "#0055FF"}
            entry.config(bg="#FFFFFF", fg="#0055FF")
        else:
            entry.insert(0, str(old_val))
            if not SudokuValidator.is_valid_move(self.board.grid, row, col, old_val):
                self.cell_states[row][col] = {"bg": "#FFEBEE", "fg": "#D32F2F"}
                entry.config(bg="#FFEBEE", fg="#D32F2F")
            else:
                self.cell_states[row][col] = {"bg": "#E8F5E9", "fg": "#2E7D32"}
                entry.config(bg="#E8F5E9", fg="#2E7D32")

        entry.config(validate="key")
        self.status_label.config(text=f"Undo: Reverted Row {row+1}, Col {col+1}.", fg="black")
        self._on_cell_focus(row, col)

    def redo_move(self):
        if not self.redo_stack or not self.board:
            self.status_label.config(text="Redo: No moves to redo.", fg="black")
            return

        row, col, old_val, new_val = self.redo_stack.pop()
        self.history.append((row, col, old_val, new_val))

        self.board.set_val(row, col, new_val)
        entry = self.entries[row][col]

        entry.config(validate="none")
        entry.delete(0, tk.END)

        if new_val == 0:
            self.cell_states[row][col] = {"bg": "#FFFFFF", "fg": "#0055FF"}
            entry.config(bg="#FFFFFF", fg="#0055FF")
        else:
            entry.insert(0, str(new_val))
            if not SudokuValidator.is_valid_move(self.board.grid, row, col, new_val):
                self.cell_states[row][col] = {"bg": "#FFEBEE", "fg": "#D32F2F"}
                entry.config(bg="#FFEBEE", fg="#D32F2F")
            else:
                self.cell_states[row][col] = {"bg": "#E8F5E9", "fg": "#2E7D32"}
                entry.config(bg="#E8F5E9", fg="#2E7D32")

        entry.config(validate="key")
        self.status_label.config(text=f"Redo: Applied Row {row+1}, Col {col+1}.", fg="black")
        self._on_cell_focus(row, col)

    def _handle_victory(self):
        self._stop_timer()
        elapsed = self.timer_seconds - 1 if self.timer_seconds > 0 else 0
        total_time = self._get_formatted_time()
        diff = self.difficulty_var.get().lower()

        current_best = self.high_scores.get(diff)
        is_new_record = current_best is None or elapsed < current_best

        if is_new_record:
            self.high_scores[diff] = elapsed
            self._save_high_scores()
            self.best_label.config(text=f"Best: {self._format_seconds(elapsed)}")
            messagebox.showinfo(
                "New Best Record!",
                f"Congratulations! You set a NEW RECORD for {diff.capitalize()} difficulty in {total_time}!"
            )
            self.status_label.config(text=f"NEW RECORD! Solved in {total_time}!", fg="green")
        else:
            messagebox.showinfo(
                "Success",
                f"Congratulations! You solved the Sudoku puzzle in {total_time}!"
            )
            self.status_label.config(text=f"Puzzle Completed Successfully in {total_time}!", fg="green")

    def get_hint(self):
        if not self.board or self.board.is_complete():
            return

        # Solve a copy of the original board to obtain solution
        solution_grid = [row[:] for row in self.board.original_grid]
        if not SudokuSolver.solve(solution_grid):
            self.status_label.config(text="Cannot generate hint for invalid board.", fg="red")
            return

        # Find first empty or incorrect cell
        for r in range(9):
            for c in range(9):
                current_val = self.board.get_val(r, c)
                correct_val = solution_grid[r][c]

                if current_val != correct_val:
                    self.history.append((r, c, current_val, correct_val))
                    self.redo_stack.clear()

                    self.board.set_val(r, c, correct_val)
                    entry = self.entries[r][c]

                    entry.config(validate="none")
                    entry.delete(0, tk.END)
                    entry.insert(0, str(correct_val))

                    # Purple Hint Highlight
                    self.cell_states[r][c] = {"bg": "#F3E5F5", "fg": "#7B1FA2"}
                    entry.config(bg="#F3E5F5", fg="#7B1FA2", state="normal")
                    entry.config(validate="key")

                    self.status_label.config(
                        text=f"Hint: Placed correct number {correct_val} at Row {r+1}, Col {c+1}.",
                        fg="#7B1FA2"
                    )

                    if self.board.is_complete():
                        self._handle_victory()
                    return

    def new_game(self):
        diff = self.difficulty_var.get().lower()
        puzzle_grid = PuzzleGenerator.generate_puzzle(diff)
        self.board = SudokuBoard(puzzle_grid)
        self.history.clear()
        self.redo_stack.clear()
        self._update_gui_from_board()
        self._start_timer()
        self._on_difficulty_changed()
        self.status_label.config(
            text=f"New Game Started. Difficulty: {diff.capitalize()}",
            fg="black"
        )

    def reset_board(self):
        if not self.board:
            return
        self.history.clear()
        self.redo_stack.clear()
        for r in range(9):
            for c in range(9):
                if not self.board.is_original(r, c):
                    self.board.set_val(r, c, 0)
        self._update_gui_from_board()
        self._start_timer()
        self.status_label.config(text="Board reset to initial state. Timer restarted.", fg="black")

    def solve_puzzle(self):
        if not self.board:
            return

        grid_to_solve = [row[:] for row in self.board.grid]
        if SudokuSolver.solve(grid_to_solve):
            self.board.grid = grid_to_solve
            self._update_gui_from_board(solving=True)
            self._stop_timer()
            total_time = self._get_formatted_time()
            self.status_label.config(text=f"Puzzle solved by Backtracking AI in {total_time}.", fg="green")
            messagebox.showinfo("Solved", f"Puzzle solved successfully in {total_time}!")
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
                    self.cell_states[r][c] = {"bg": "#E0E0E0", "fg": "#111111"}
                    entry.config(
                        bg="#E0E0E0",
                        fg="#111111",
                        state="disabled",
                        disabledbackground="#E0E0E0",
                        disabledforeground="#111111"
                    )
                else:
                    if solving:
                        self.cell_states[r][c] = {"bg": "#E8F8F5", "fg": "#27AE60"}
                        entry.config(
                            bg="#E8F8F5",
                            fg="#27AE60",
                            state="normal"
                        )
                    else:
                        self.cell_states[r][c] = {"bg": "#FFFFFF", "fg": "#0055FF"}
                        entry.config(
                            bg="#FFFFFF",
                            fg="#0055FF",
                            state="normal"
                        )

                entry.config(validate="key")
