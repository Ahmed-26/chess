# ♟️ Chess Application - Professional Setup Guide

A full-stack chess application featuring a **ReactJS + Material-UI frontend** with a **FastAPI backend** powered by a sophisticated Python chess engine.

**Play against AI with undo functionality, move history tracking, and captured pieces visualization.**

---

## 📋 Table of Contents

- [System Requirements](#-system-requirements)
- [Project Structure](#-project-structure)
- [Run This Project](#run-this-project)
- [Installation](#-installation-step-by-step)
- [Running the Application](#-running-the-application)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Development Notes](#-development-notes)

---

## 💻 System Requirements

- **Python 3.10+**
- **Node.js 16+** and **npm 8+**
- **Windows/Mac/Linux** with PowerShell or Bash

---

## 📁 Project Structure

```
chess/
├── api_server.py              # FastAPI backend (chess engine REST API)
├── board.py                   # Board class (8x8 grid, move execution)
├── piece.py                   # Piece classes (Pawn, Rook, Knight, etc.)
├── move.py                    # Move representation & helpers
├── move_history.py            # Move history with undo/redo (LinkedList, Stack)
├── ai_engine.py               # AI engine (minimax with memoization)
├── main.py                    # Terminal mode entry point
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
│
└── frontend/                  # React + Material-UI frontend
    ├── src/
    │   ├── App.jsx            # Main React component
    │   ├── api.js             # API client (fetch helper)
    │   ├── theme.js           # Material-UI theme
    │   ├── styles.css         # Custom styling
    │   └── main.jsx           # React entry point
    ├── index.html             # HTML template
    ├── package.json           # Node dependencies
    ├── vite.config.js         # Vite build config
    └── .gitignore             # Frontend git rules
```

---

## Run This Project

Use one of the two modes below.

### Mode A: Web App (FastAPI backend + React frontend)

1. Open PowerShell in project root:

```powershell
cd E:\University\4th_Semester\ACP\Project\chess
```

2. Create/activate venv and install backend dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

3. Start backend (Terminal 1):

```powershell
cd E:\University\4th_Semester\ACP\Project\chess
uvicorn api_server:app --reload
```

4. Start frontend (Terminal 2):

```powershell
cd E:\University\4th_Semester\ACP\Project\chess\frontend
npm install
npm run dev
```

5. Open in browser:

- Frontend: http://localhost:5173
- Backend docs: http://127.0.0.1:8000/docs

### Mode B: Terminal Chess (Python only)

```powershell
cd E:\University\4th_Semester\ACP\Project\chess
.\.venv\Scripts\Activate.ps1
python main.py
```

### Common Mistake

If you run `python main.py` inside the `frontend` folder, it fails because `main.py` is in the project root. Go back to root first:

```powershell
cd E:\University\4th_Semester\ACP\Project\chess
python main.py
```

---

## 🚀 Installation (Step-by-Step)

### Step 1: Clone/Navigate to Project

```powershell
cd e:\University\3rd_Semester\chess
```

### Step 2: Set Up Python Virtual Environment

```powershell
# Create virtual environment
python -m venv .venv

# Activate it (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# If you get execution policy error, run:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Python Dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages:**

- `fastapi==0.115.12`
- `uvicorn==0.34.2`
- `pydantic==2.12.5`

### Step 4: Install Frontend Dependencies

```powershell
cd frontend
npm install
cd ..
```

---

## ▶️ Running the Application

### **Option A: Full Stack (Recommended)**

#### Terminal 1 - Start Backend Server

```powershell
# Make sure you're in the project root and venv is activated
uvicorn api_server:app --reload
```

**Expected output:**

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

#### Terminal 2 - Start Frontend Development Server

```powershell
cd frontend
npm run dev
```

**Expected output:**

```
  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

#### Step 3: Open in Browser

- Open your browser and navigate to: **`http://localhost:5173`**
- The frontend will automatically connect to the backend at `http://127.0.0.1:8000`

---

### **Option B: Terminal Mode Only**

```powershell
python main.py
```

Use commands like:

- `e2 e4` - Move piece
- `undo` - Undo last move
- `ai on/off` - Toggle AI opponent
- `quit` - Exit game

---

## ✨ Features

### Frontend Features

- ✅ **Interactive Chess Board** - Click to move pieces
- ✅ **AI Opponent** - Toggle AI on/off, plays as Black
- ✅ **Move History** - Track all moves with move numbering
- ✅ **Undo/Redo** - Revert moves at any time
- ✅ **Captured Pieces Display** - Black captures on left, White on right
- ✅ **Responsive Design** - Works on desktop and mobile (600px, 480px breakpoints)
- ✅ **Legal Move Highlighting** - Green highlights for valid moves
- ✅ **Real-time Status** - Game status, turn indicator, AI toggle buttons

### Backend Features

- ✅ **FastAPI REST Server** - High-performance async backend
- ✅ **Chess Engine** - Complete chess rules implementation
- ✅ **AI with Minimax** - Recursive AI with memoization
- ✅ **Move Validation** - Legal move checking for all pieces
- ✅ **Game State Management** - Full undo/redo support
- ✅ **Move History Tracking** - LinkedList-based move history

---

## 🛠️ Technology Stack

| Layer               | Technology    | Version  |
| ------------------- | ------------- | -------- |
| **Frontend**        | React         | 19.1.0   |
| **UI Library**      | Material-UI   | 7.1.0    |
| **Bundler**         | Vite          | 6.3.5    |
| **Styling**         | Emotion + CSS | Latest   |
| **Backend**         | FastAPI       | 0.115.12 |
| **Server**          | Uvicorn       | 0.34.2   |
| **Validation**      | Pydantic      | 2.12.5   |
| **Language**        | Python        | 3.10+    |
| **Package Manager** | npm           | 8.0+     |

---

## 💡 Development Notes

### Backend API Endpoints

| Method | Endpoint              | Purpose                      |
| ------ | --------------------- | ---------------------------- |
| `GET`  | `/api/state`          | Get current board state      |
| `POST` | `/api/move`           | Execute a move               |
| `POST` | `/api/undo`           | Undo last move               |
| `POST` | `/api/reset`          | Reset game                   |
| `GET`  | `/api/legal/{square}` | Get legal moves for a square |
| `POST` | `/api/command`        | Execute commands (ai on/off) |

### Key Files Explained

- **api_server.py**: FastAPI wrapper around chess engine. Manages game state, API routes, and AI coordination.
- **board.py**: 8x8 board representation. Handles move execution and legality checking.
- **piece.py**: Base `Piece` class and subclasses for each piece type. Move generation logic per piece.
- **move_history.py**: LinkedList-based move history with undo/redo stacks.
- **ai_engine.py**: Minimax algorithm with depth-based move evaluation and memoization cache.

### Debugging

- **Backend logs**: Check terminal running Uvicorn for request logs and errors
- **Frontend logs**: Open browser DevTools (F12) → Console tab
- **API Testing**: Use Postman or visit `http://127.0.0.1:8000/docs` for Swagger UI

### Common Issues

| Issue                      | Solution                                                          |
| -------------------------- | ----------------------------------------------------------------- |
| `Port 5173 already in use` | Change port: `npm run dev -- --port 5174`                         |
| `Port 8000 already in use` | Use different port: `uvicorn api_server:app --port 8001 --reload` |
| `Module not found`         | Reinstall: `pip install -r requirements.txt`                      |
| `npm ERR`                  | Clear cache: `npm cache clean --force && npm install`             |
| `CORS errors`              | Backend already configured with CORS headers                      |

---

## 🔧 Build for Production

### Frontend Build

```powershell
cd frontend
npm run build
# Output in frontend/dist/
```

### Backend Deployment

```powershell
# Production server (remove --reload)
uvicorn api_server:app --host 0.0.0.0 --port 8000
```

---

## 📚 Learning Concepts (OOP & DSA)

This project demonstrates:

- **Object-Oriented Programming**: Piece hierarchy, Board class, Move objects
- **Data Structures**: LinkedList (move history), Stack (undo), Queue concepts
- **Algorithms**: Minimax (game theory), Memoization (dynamic programming)
- **Design Patterns**: API wrapper pattern, Factory pattern for pieces
- **Full-Stack Development**: REST API, State management, UI components

---

## 📝 License

Educational project for learning OOP, DSA, and Full-Stack Development.

---

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
