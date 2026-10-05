# Sudoku Game & Solver

A clean-architecture, interactive Sudoku game and automatic backtracking solver built in Python. Designed with modularity, object-oriented design, and clean code standards.

---

## Key Features

- **Interactive CLI Interface**: Clean, formatted 9x9 board rendering with row/column labels and visual separators.
- **Automatic Sudoku Solver**: Integrated AI solver using the **Backtracking Depth-First Search Algorithm**.
- **Dynamic Puzzle Generator**: Generates unique, valid, and guaranteed solvable puzzles across difficulty modes (**Easy**, **Medium**, **Hard**).
- **Rule Validator**: Built-in validation checking moves against standard Sudoku constraints (Row, Column, 3x3 Sub-grid).
- **Clean Architecture**: Strict separation of concerns (Core Logic, Board Model, Solver Algorithm, Generator, UI).

---

## Project Directory Structure

```text
Sudoku Game/
│
├── main.py                      # Application entry point
├── README.md                    # Project documentation
├── .gitignore                   # Git untracked rules configuration
│
└── src/                         # Source package directory
    ├── core/                    # Core business logic module
    │   ├── board.py             # 9x9 Grid matrix data model & state management
    │   ├── validator.py         # Sudoku rule validation
    │   └── solver.py            # Backtracking depth-first search solver algorithm
    │
    ├── generator/               # Generator module
    │   └── puzzle_generator.py  # Generates puzzles with difficulty settings
    │
    └── ui/                      # Interface layer module
        └── cli_ui.py            # Terminal display & game control loop
```

---

## Quick Start Guide

### Prerequisites
- Python 3.8 or higher installed on your system.

### Running the Game

Run the following command from the project root directory:

```bash
python main.py
```

---

## Game Commands

During gameplay, interact with the board using the following commands:

| Command | Syntax | Description | Example |
| :--- | :--- | :--- | :--- |
| **Set Cell** | `set <row> <col> <val>` | Place a number (1-9) at Row (1-9) and Column (1-9) | `set 3 7 5` |
| **Solve Puzzle** | `solve` | Instantly solve the current puzzle using Backtracking AI | `solve` |
| **Quit Game** | `quit` | Exit the application | `quit` |

---

## Technical Algorithm Detail (Backtracking)

The solver utilizes a recursive **Depth-First Search (DFS) Backtracking Algorithm**:
1. **Find Unassigned Cell**: Scans grid for the next empty position (`0`).
2. **Constraint Check**: Attempts numbers `1-9` sequentially, checking row, column, and 3x3 block validity via `SudokuValidator`.
3. **Recursion & Backtrack**: If valid, places the candidate number and recursively attempts to solve the rest of the board. If a dead-end occurs, resets the cell (`0`) and backtracks to evaluate the next number.
