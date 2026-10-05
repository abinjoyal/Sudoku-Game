# Sudoku Game & Solver

A clean-architecture, interactive Graphical Desktop Sudoku game and automatic backtracking solver built in Python. Designed with modularity, object-oriented design, and clean code standards.

---

## Key Features

- **Graphical User Interface (GUI)**: Built using Python Tkinter, providing a clean 9x9 grid with 3x3 sub-grid borders.
- **Move History (Undo / Redo)**: Step-by-step move history with global keyboard shortcuts (`Ctrl+Z` to Undo, `Ctrl+Y` to Redo).
- **Same-Number Focus Highlight Guide**: Selecting any number on the grid automatically highlights all matching instances in soft cyan for quick scanning.
- **Get Hint System**: Built-in intelligent hint generator that places the next correct number using the Backtracking solver algorithm.
- **Real-Time Visual Validation**: Dynamic cell color highlighting (Red background/text for invalid moves, Green background/text for correct moves).
- **Live Stopwatch & Completion Timer**: Real-time timer tracking game duration and recording final completion time upon solving.
- **High Score Persistence**: Automatically saves your best completion times per difficulty level in `data/high_scores.json`.
- **Automatic Sudoku Solver**: Integrated AI solver powered by the **Backtracking Depth-First Search Algorithm**.
- **Dynamic Puzzle Generator**: Generates unique, valid, and guaranteed solvable puzzles across difficulty modes (**Easy**, **Medium**, **Hard**).
- **Clean Architecture**: Strict separation of concerns (Core Logic, Board Model, Solver Algorithm, Generator, UI Layer).

---

## Project Directory Structure

```text
Sudoku Game/
│
├── main.py                      # Application entry point
├── README.md                    # Project documentation
├── .gitignore                   # Git untracked rules configuration
│
├── data/                        # Local data storage directory
│   └── high_scores.json        # Best time records per difficulty
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
        ├── gui_ui.py            # Tkinter Graphical Desktop UI with Timer, Color Feedback, Undo/Redo & Hints
        └── cli_ui.py            # Command Line Interface (CLI)
```

---

## Quick Start Guide

### Prerequisites
- Python 3.8 or higher installed on your system.

### Running the Application

Run the following command from the project root directory:

```bash
python main.py
```

---

## Desktop GUI Features & Controls

- **Undo / Redo System**:
  - **Undo (`Ctrl + Z`)**: Revert previous moves step-by-step.
  - **Redo (`Ctrl + Y`)**: Re-apply undone moves.
- **Same-Number Highlight**: Click any filled cell to highlight all matching numbers on the board in soft cyan.
- **Get Hint**: Automatically fills in the correct number for the next unassigned cell.
- **Real-Time Color Feedback**:
  - **Red Cell**: Indicates an invalid move that conflicts with another number in the same Row, Column, or 3x3 Box.
  - **Green Cell**: Indicates a valid placement adhering to Sudoku rules.
  - **Purple Cell**: Indicates a number placed by the Hint System.
  - **Locked Gray Cell**: Pre-filled puzzle numbers.
- **Difficulty Selector**: Select between Easy, Medium, or Hard difficulty before starting a new game.
- **New Game**: Generates a new Sudoku puzzle and starts the live timer (`Time: 00:00`).
- **Solve Puzzle**: Automatically solves the current board configuration using Backtracking AI and records completion time.
- **Reset**: Restores the current puzzle to its initial state and restarts the timer.

---

## Technical Algorithm Detail (Backtracking)

The solver utilizes a recursive **Depth-First Search (DFS) Backtracking Algorithm**:
1. **Find Unassigned Cell**: Scans grid for the next empty position (`0`).
2. **Constraint Check**: Attempts numbers `1-9` sequentially, checking row, column, and 3x3 block validity via `SudokuValidator`.
3. **Recursion & Backtrack**: If valid, places the candidate number and recursively attempts to solve the rest of the board. If a dead-end occurs, resets the cell (`0`) and backtracks to evaluate the next number.
