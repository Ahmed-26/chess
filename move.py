"""move.py
Move dataclass storing a chess move.

DSA Concepts in this file:
- Data class used to represent a move (structured data).
"""

from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Move:
  # Represent a chess move.  
    """
    Attributes:
        from_pos: tuple (row, col)
        to_pos: tuple (row, col)
        piece_moved: str representation or object
        piece_captured: Optional[str]
        notation: Simple algebraic-like string
    """

    from_pos: Tuple[int, int]
    to_pos: Tuple[int, int]
    piece_moved: object
    piece_captured: Optional[object] = None
    notation: str = ""

    def __str__(self):
        return (
            self.notation
            or f"{self.pos_to_alg(self.from_pos)} {self.pos_to_alg(self.to_pos)}"
        )

    @staticmethod
    def pos_to_alg(pos):
        # Convert (row, col) to algebraic (e.g., (6,4) -> e2)
        r, c = pos
        return f"{chr(ord('a') + c)}{8 - r}"
