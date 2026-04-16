# Chess Terminal (OOP + DSA Edition)

This is a terminal-based chess game written in Python with a strong focus on demonstrating
Object-Oriented Programming (OOP) and Data Structures & Algorithms (DSA) concepts.

## Quick start

Install dependencies and run the game from the project root or the `chess` directory.

1. Install Python dependencies listed in `requirements.txt`:

```powershell
pip install -r requirements.txt
```

1. Run the terminal game (wrapper runs the internal entrypoint):

```powershell
python main.py
```

1. Run the web GUI backend (FastAPI):

```powershell
uvicorn api_server:app --reload
```

1. Run the React + Material UI frontend:

```powershell
cd frontend
npm install
npm run dev
```

Then open `http://localhost:5173`.

Or run the GUI (Pygame) frontend from the `chess` folder:

```powershell
cd chess_terminal
python pygame_gui.py
```

## Project structure (code structure)

chess/

- main.py # convenience runner (runs chess_terminal/main.py)
- requirements.txt # third-party dependencies to install with pip
- README.md # this file
- chess_terminal/
  - main.py # terminal game entrypoint (text-based UI)
  - pygame_gui.py # optional Pygame frontend (click-to-move GUI)
  - board.py # Board class (8x8 array), move execution and legality
  - piece.py # Piece base class and subclasses (Pawn,Rook,...) with move generation
  - move.py # Move dataclass and helpers
  - move_history.py # LinkedList, Stack, Queue for history/undo/turns
  - ai_engine.py # AI: greedy + minimax (recursion, memoization)
  - utils/ helpers.py # sorting/search helpers (quicksort, binary/linear search)

## Installation

1. (Optional) Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

1. Install dependencies:

```powershell
pip install -r requirements.txt
```

If you only want the Pygame GUI, installing `pygame` is sufficient:

```powershell
pip install pygame
```

## How to run

- Terminal (text) mode from project root:

```powershell
python main.py
```

- Pygame GUI (from project root):

```powershell
python -m chess_terminal.pygame_gui
```

- React + MUI web GUI:

```powershell
# terminal 1 (project root)
uvicorn api_server:app --reload

# terminal 2
cd frontend
npm install
npm run dev
```

Or change directory and run the script directly:

```powershell
cd chess_terminal
python pygame_gui.py
```

## Short summary (what this project provides)

- A playable terminal-based chess program demonstrating OOP and common DSA concepts.
- Play modes: Player vs Player (text), optional AI opponent (greedy/minimax).
- Undo/Redo and move history implemented using Stack and LinkedList.
- Board represented as a 2D list (array) for O(1) access; move generation uses piece classes.
- AI demonstrates recursion/backtracking (minimax), move sorting, and memoization (simple transposition cache).

## Short notes (Hindi)

- Install karne ke liye: `pip install -r requirements.txt`.
- Terminal se chalane ke liye root pe `python main.py` likhen.
- GUI chahiye to `python -m chess_terminal.pygame_gui` ya `cd chess_terminal` phir `python pygame_gui.py`.
- Code structure upar di hui hai — har file ka ek-line purpose bhi diya gaya hai.

Commands inside the game:

- e2 e4 -- move
- undo -- undo last move
- redo -- redo last undone move
- history -- view move history
- ai on/off -- toggle AI for Black
- ai depth [n] -- set minimax depth

Commands inside the web GUI command box:

- e2 e4 -- move
- undo -- undo last move
- redo -- redo last undone move
- history -- show move history
- ai on/off -- toggle AI for Black
- ai depth [n] -- set minimax depth
- reset -- start a new game

## DSA Concepts and where they are used

- Arrays (Lists): `board.py` uses a 2D list (8x8) to store the board. Comment: "Using a 2D array to store board state for O(1) piece lookup."
- Linked List: `move_history.py` provides `MoveLinkedList` (doubly-linked) storing moves. Comment: "Linked List used to store move history with easy undo traversal."
- Stack: `move_history.py` provides `Stack` used for undo/redo. Comment: "Stack used to revert the last move efficiently."
- Queue: `move_history.py` provides `TurnQueue` used to alternate turns. Comment: "Queue used to manage alternating player turns."
- Tree: `ai_engine.py` includes `TreeNode` and minimax explores a game tree. Comment: "Tree structure used to simulate future game states."
- Graph: `board.py` logic treats moves as edges from a square to target squares; comments indicate graph usage. Comment: "Graph used to map piece movement possibilities from one position to another."
- Hash Table (Dictionary): `board.py` and `ai_engine.py` use `eval_cache` for memoization of evaluations. Comment: "Hash Table used as transposition cache for repeated positions."
- Sorting Algorithms: `utils/helpers.py` contains a Quick Sort implementation used by the AI to order moves. Comment: "Sorting moves by heuristic score using Quick Sort."
- Searching Algorithms: `utils/helpers.py` contains `binary_search` and `linear_search`. Comments show where they'd be applied. Comment: "Binary search used to quickly find a specific move."
- Recursion & Backtracking: `ai_engine.py` minimax uses recursion and simulates moves (apply/undo). Comment: "Recursive backtracking used in AI decision-making."
- Greedy Algorithm: `ai_engine.greedy_move` demonstrates a simple greedy immediate-capture heuristic. Comment: "Greedy choice: AI selects best immediate move by material advantage."
- Dynamic Programming (Memoization): `ai_engine.minimax` and `board.evaluate_material` cache evaluations. Comment: "DP applied to store and reuse evaluation scores for positions."

## Notes

This project is intentionally educational: some chess rules are simplified (e.g., no castling, en-passant, or pawn promotion mechanics beyond base move generation). The code includes comments that point to the DSA concept being demonstrated.

Feel free to extend the rules and add more sophisticated AI or UI as an exercise.
