"""ai_engine.py
Provides simple AI: greedy immediate move and a minimax search with recursion, tree nodes, memoization, and move sorting.

DSA Concepts:
- Tree: TreeNode used to represent game state tree during minimax.
  # Tree structure used to simulate future game states.
- Recursion & Backtracking: minimax explores moves recursively.
  # Recursive backtracking used in AI decision-making.
- Dynamic Programming (Memoization): caching board evaluations.
  # DP applied to store and reuse evaluation scores for positions.
- Greedy Algorithm: fast heuristic for immediate move selection.
  # Greedy choice: AI selects best immediate move by material advantage.
- Sorting: moves sorted by heuristic (quicksort from helpers).
  # Sorting moves by heuristic score using Quick Sort.
"""

from typing import List, Tuple, Optional
import board as board_mod
from move import Move
import utils.helpers as helpers


class TreeNode:
    """Simple tree node representing a board state and the move that led to it."""

    def __init__(self, board: board_mod.Board, move: Optional[Move] = None):
        self.board = board
        self.move = move
        self.children: List["TreeNode"] = []


PIECE_VALUES = {
    "♙": 1,
    "♟": -1,
    "♖": 5,
    "♜": -5,
    "♘": 3,
    "♞": -3,
    "♗": 3,
    "♝": -3,
    "♕": 9,
    "♛": -9,
    "♔": 1000,
    "♚": -1000,
}


def evaluate_material(b: board_mod.Board) -> int:
    """Simple material evaluation: positive if good for white, negative for black.

    Uses Hash Table (board.eval_cache) to store results.
    # Hash Table used as transposition cache for repeated positions.
    """
    key = b.board_key()
    if key in b.eval_cache:
        return b.eval_cache[key]
    score = 0
    for r in range(8):
        for c in range(8):
            p = b.get_piece((r, c))
            if p is not None:
                ch = p.symbol()
                score += PIECE_VALUES.get(ch, 0)
    b.eval_cache[key] = score
    return score


def greedy_move(
    b: board_mod.Board, color: str
) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """Choose the best immediate move by material gain (greedy).

    # Greedy choice: AI selects best immediate move by material advantage.
    """
    moves = b.generate_legal_moves(color)
    best = None
    best_score = -9999 if color == "w" else 9999
    for frm, to in moves:
        captured = b.get_piece(to)
        value = 0
        if captured is not None:
            value = PIECE_VALUES.get(captured.symbol(), 0)
        if color == "w":
            if value > best_score:
                best_score = value
                best = (frm, to)
        else:
            if value < best_score:
                best_score = value
                best = (frm, to)
    return best


def minimax(
    b: board_mod.Board,
    depth: int,
    maximizing: bool,
    alpha: int = -99999,
    beta: int = 99999,
    memo=None,
) -> Tuple[int, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
    """Minimax with alpha-beta pruning and memoization.

    Recursively explores the tree of moves to given depth. Uses memo dict keyed by board_key.
    `maximizing=True` means White is evaluating, `maximizing=False` means Black.
    """
    if memo is None:
        memo = {}

    key = (b.board_key(), depth, maximizing)
    if key in memo:
        return memo[key]

    if depth == 0:
        val = evaluate_material(b)
        return val, None

    color = "w" if maximizing else "b"
    moves = b.generate_legal_moves(color)

    # Sort moves by heuristic so we search good moves first (improves pruning)
    def move_score(mv):
        frm, to = mv
        captured = b.get_piece(to)
        return PIECE_VALUES.get(captured.symbol(), 0) if captured else 0

    # Sorting demonstration using Quick Sort
    moves = helpers.quicksort(moves, key=move_score)

    best_move = None
    if maximizing:
        max_eval = -99999
        for frm, to in moves:
            # Apply/undo directly on the same board to avoid allocating copies per node.
            piece_moved = b.get_piece(frm)
            captured = b.get_piece(to)
            b.set_piece(to, piece_moved)
            b.set_piece(frm, None)
            b.to_move = "b"
            val, _ = minimax(b, depth - 1, False, alpha, beta, memo)
            # Restore board state exactly for sibling branches.
            b.set_piece(frm, piece_moved)
            b.set_piece(to, captured)
            b.to_move = "w"
            if val > max_eval:
                max_eval = val
                best_move = (frm, to)
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        memo[key] = (max_eval, best_move)
        return memo[key]
    else:
        min_eval = 99999
        for frm, to in moves:
            # Same in-place simulation for the minimizing side.
            piece_moved = b.get_piece(frm)
            captured = b.get_piece(to)
            b.set_piece(to, piece_moved)
            b.set_piece(frm, None)
            b.to_move = "w"
            val, _ = minimax(b, depth - 1, True, alpha, beta, memo)
            b.set_piece(frm, piece_moved)
            b.set_piece(to, captured)
            b.to_move = "b"
            if val < min_eval:
                min_eval = val
                best_move = (frm, to)
            beta = min(beta, val)
            if beta <= alpha:
                break
        memo[key] = (min_eval, best_move)
        return memo[key]
