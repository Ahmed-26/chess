"""board.py
Board class using a 2D list (array) to store pieces and provide core game logic.

DSA Concepts:
- Arrays (Lists): 8x8 board is a 2D list for O(1) piece access.
  # Using a 2D array to store board state for O(1) piece lookup.
- Graph: adjacency mapping from squares to legal-target squares (used for move/attack analysis).
  # Graph used to map piece movement possibilities from one position to another.
- Hash Table: board state string used as key in caches (transposition table).
  # Hash Table used as transposition cache for repeated positions.
"""

from typing import List, Optional, Tuple
from copy import deepcopy
import piece
from move import Move

Position = Tuple[int, int]


class Board:
    def __init__(self):
        # 8x8 array: rows 0..7, cols 0..7
        # White pieces will be at the bottom (rows 6 and 7)
        self.board: List[List[Optional[piece.Piece]]] = [
            [None for _ in range(8)] for _ in range(8)
        ]
        self.to_move = "w"  # current side to move
        # Graph adjacency cache: maps pos -> list of reachable pos for current piece placements
        self._graph = {}
        # Transposition cache for evaluations
        self.eval_cache = (
            {}
        )  # Hash Table used as transposition cache for repeated positions.
        self.setup_board()

    def setup_board(self):
        # Place pawns
        for c in range(8):
            self.board[6][c] = piece.Pawn("w")
            self.board[1][c] = piece.Pawn("b")
        # Other pieces
        order = [
            piece.Rook,
            piece.Knight,
            piece.Bishop,
            piece.Queen,
            piece.King,
            piece.Bishop,
            piece.Knight,
            piece.Rook,
        ]
        for c, cls in enumerate(order):
            self.board[7][c] = cls("w")
            self.board[0][c] = cls("b")

    def in_bounds(self, pos: Position) -> bool:
        r, c = pos
        return 0 <= r < 8 and 0 <= c < 8

    def get_piece(self, pos: Position) -> Optional[piece.Piece]:
        r, c = pos
        return self.board[r][c]

    def set_piece(self, pos: Position, p: Optional[piece.Piece]):
        r, c = pos
        self.board[r][c] = p

    def move_piece(self, from_pos: Position, to_pos: Position) -> Move:
        """Execute a move on the board and return a Move object for history/undo.

        This does not validate check legality here; higher-level code will verify.
        """
        fm = self.get_piece(from_pos)
        captured = self.get_piece(to_pos)
        self.set_piece(to_pos, fm)
        self.set_piece(from_pos, None)
        mv = Move(from_pos, to_pos, fm, captured)
        # Flip side to move
        self.to_move = "b" if self.to_move == "w" else "w"
        # Update graph cache lazily
        self._graph = {}
        return mv

    def undo_move(self, move: Move):
        # Reverse execution (basic undo)
        self.set_piece(move.from_pos, move.piece_moved)
        self.set_piece(move.to_pos, move.piece_captured)
        self.to_move = move.piece_moved.color
        self._graph = {}

    def find_king(self, color: str) -> Optional[Position]:
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p is not None and isinstance(p, piece.King) and p.color == color:
                    return (r, c)
        return None

    def is_under_attack(self, pos: Position, by_color: str) -> bool:
        """Check if a square is attacked by any piece of by_color.

        This uses generated moves for opponent pieces (graph-like traversal).
        # Graph used to map piece movement possibilities from one position to another.
        """
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p is not None and p.color == by_color:
                    moves = p.get_moves(self, (r, c))
                    if pos in moves:
                        return True
        return False

    def is_in_check(self, color: str) -> bool:
        king_pos = self.find_king(color)
        if king_pos is None:
            return True  # No king found means captured - treat as check
        return self.is_under_attack(king_pos, "b" if color == "w" else "w")

    def generate_legal_moves(self, color: str):
        """Generate all pseudo-legal moves for color and filter out moves that leave king in check.

        Returns list of Move objects (not Move dataclass yet; simple tuples converted later).
        """
        moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p is not None and p.color == color:
                    for to in p.get_moves(self, (r, c)):
                        # Simulate in-place and roll back immediately.
                        # This is faster than deep-copying the board for every candidate move.
                        saved_from = self.get_piece((r, c))
                        saved_to = self.get_piece(to)
                        self.set_piece(to, saved_from)
                        self.set_piece((r, c), None)
                        in_check = self.is_in_check(color)
                        # Undo
                        self.set_piece((r, c), saved_from)
                        self.set_piece(to, saved_to)
                        if not in_check:
                            moves.append(((r, c), to))
        return moves

    def board_key(self) -> str:
        """Create a simple hashable string for transposition cache.

        This is not a Zobrist hash but sufficient for educational memoization.
        # Hash Table used as transposition cache for repeated positions.
        """
        chars = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p is None:
                    chars.append(".")
                else:
                    ch = p.symbol()
                    # normalize to single char (take first byte)
                    chars.append(ch)
        return "".join(chars) + self.to_move

    def copy(self):
        # Shallow copy of pieces is OK because Piece instances are immutable in this design
        newb = Board.__new__(Board)
        newb.board = deepcopy(self.board)
        newb.to_move = self.to_move
        newb._graph = dict(self._graph)
        newb.eval_cache = dict(self.eval_cache)
        return newb

    def print_board(self):
        # ASCII board print with rank (1-8) and file (a-h) labels.
        # Ranks on the left (8..1). Files on the bottom (a..h).
        # This improves usability when entering moves like 'e2 e4'.
        for r in range(8):
            row_pieces = []
            for c in range(8):
                p = self.board[r][c]
                row_pieces.append(p.symbol() if p is not None else ".")
            # Print rank number at the start of the row
            print(f"{8 - r} " + " ".join(row_pieces))

        # Print file letters beneath the board with matching spacing
        files = " ".join([chr(ord("a") + c) for c in range(8)])
        print("  " + files)
