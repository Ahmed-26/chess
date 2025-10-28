"""piece.py
Defines Piece base class and all derived chess piece classes.

DSA Concepts used here:
- Polymorphism and OOP: base Piece with derived classes.
- Graph concept: legal moves are edges from a position to target positions (see comment in Board where graph uses these).
"""

from typing import List, Tuple

Position = Tuple[int, int]


class Piece:
    """Base class for chess pieces.

    Subclasses must implement `get_moves(board, pos)` returning list of target positions.
    """

    def __init__(self, color: str):
        self.color = color  # 'w' or 'b'

    def symbol(self) -> str:
        raise NotImplementedError

    def get_moves(self, board, pos: Position) -> List[Position]:
        raise NotImplementedError

    def opposite(self):
        return "b" if self.color == "w" else "w"


class Pawn(Piece):
    def symbol(self):
        return "♙" if self.color == "w" else "♟"

    def get_moves(self, board, pos):
        moves = []
        r, c = pos
        direction = -1 if self.color == "w" else 1
        # One step
        nr = r + direction
        if board.in_bounds((nr, c)) and board.get_piece((nr, c)) is None:
            moves.append((nr, c))
            # Two step from starting rank
            start_row = 6 if self.color == "w" else 1
            nr2 = r + 2 * direction
            if r == start_row and board.get_piece((nr2, c)) is None:
                moves.append((nr2, c))
        # Captures
        for dc in (-1, 1):
            nc = c + dc
            if board.in_bounds((nr, nc)):
                target = board.get_piece((nr, nc))
                if target is not None and target.color != self.color:
                    moves.append((nr, nc))
        return moves


class Rook(Piece):
    def symbol(self):
        return "♖" if self.color == "w" else "♜"

    def get_moves(self, board, pos):
        # Sliding moves in 4 directions
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr
                c += dc
                if not board.in_bounds((r, c)):
                    break
                occupant = board.get_piece((r, c))
                if occupant is None:
                    moves.append((r, c))
                else:
                    if occupant.color != self.color:
                        moves.append((r, c))
                    break
        return moves


class Knight(Piece):
    def symbol(self):
        return "♘" if self.color == "w" else "♞"

    def get_moves(self, board, pos):
        moves = []
        deltas = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]
        r, c = pos
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            if board.in_bounds((nr, nc)):
                target = board.get_piece((nr, nc))
                if target is None or target.color != self.color:
                    moves.append((nr, nc))
        return moves


class Bishop(Piece):
    def symbol(self):
        return "♗" if self.color == "w" else "♝"

    def get_moves(self, board, pos):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        for dr, dc in directions:
            r, c = pos
            while True:
                r += dr
                c += dc
                if not board.in_bounds((r, c)):
                    break
                occupant = board.get_piece((r, c))
                if occupant is None:
                    moves.append((r, c))
                else:
                    if occupant.color != self.color:
                        moves.append((r, c))
                    break
        return moves


class Queen(Piece):
    def symbol(self):
        return "♕" if self.color == "w" else "♛"

    def get_moves(self, board, pos):
        # Combine rook and bishop
        moves = Rook.get_moves(self, board, pos) + Bishop.get_moves(self, board, pos)
        return moves


class King(Piece):
    def symbol(self):
        return "♔" if self.color == "w" else "♚"

    def get_moves(self, board, pos):
        moves = []
        r, c = pos
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if board.in_bounds((nr, nc)):
                    t = board.get_piece((nr, nc))
                    if t is None or t.color != self.color:
                        moves.append((nr, nc))
        # Castling not implemented in this educational example (would require more state tracking)
        return moves
