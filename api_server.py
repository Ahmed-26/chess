from typing import Dict, List, Optional, Tuple

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import ai_engine
from board import Board
from move import Move
from move_history import MoveLinkedList, Stack


Position = Tuple[int, int]


class MoveRequest(BaseModel):
    from_square: str
    to_square: str


class CommandRequest(BaseModel):
    command: str


class ChessGame:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.board = Board()
        self.history = MoveLinkedList()
        self.undo_stack = Stack()
        self.redo_stack = Stack()
        self.played_moves: List[Move] = []
        self.ai_enabled = False
        self.ai_depth = 2
        self.last_message = "New game started."
        self.captured_white: List[Dict] = []
        self.captured_black: List[Dict] = []

    @staticmethod
    def alg_to_pos(square: str) -> Optional[Position]:
        if len(square) != 2:
            return None
        file_part = square[0].lower()
        rank_part = square[1]
        if file_part < "a" or file_part > "h":
            return None
        if rank_part < "1" or rank_part > "8":
            return None
        col = ord(file_part) - ord("a")
        row = 8 - int(rank_part)
        return (row, col)

    @staticmethod
    def pos_to_alg(pos: Position) -> str:
        r, c = pos
        return f"{chr(ord('a') + c)}{8 - r}"

    def _piece_payload(self, pos: Position):
        piece_obj = self.board.get_piece(pos)
        if piece_obj is None:
            return None
        return {
            "symbol": piece_obj.symbol(),
            "color": piece_obj.color,
            "type": piece_obj.__class__.__name__,
            "square": self.pos_to_alg(pos),
        }

    def _board_payload(self):
        out = []
        for r in range(8):
            row = []
            for c in range(8):
                row.append(self._piece_payload((r, c)))
            out.append(row)
        return out

    def _status_text(self) -> str:
        side = "White" if self.board.to_move == "w" else "Black"
        check = self.board.is_in_check(self.board.to_move)
        if check:
            return f"{side} to move (in check)"
        return f"{side} to move"

    def _apply_move(self, from_pos: Position, to_pos: Position) -> Tuple[bool, str]:
        side = self.board.to_move
        moving_piece = self.board.get_piece(from_pos)
        if moving_piece is None:
            return False, "No piece at source square."
        if moving_piece.color != side:
            return False, "You must move your own piece."

        legal = self.board.generate_legal_moves(side)
        if (from_pos, to_pos) not in legal:
            return False, "Illegal move."

        captured = self.board.get_piece(to_pos)
        move_obj = Move(from_pos, to_pos, moving_piece, captured)
        self.board.move_piece(from_pos, to_pos)
        self.history.append(move_obj)
        self.undo_stack.push(move_obj)
        self.redo_stack.clear()
        self.played_moves.append(move_obj)

        # Track captured pieces
        if captured:
            self._piece_payload((to_pos))
            captured_info = {
                "symbol": captured.symbol(),
                "color": captured.color,
                "type": captured.__class__.__name__,
            }
            if captured.color == "w":
                self.captured_white.append(captured_info)
            else:
                self.captured_black.append(captured_info)

        return True, f"Moved {self.pos_to_alg(from_pos)} to {self.pos_to_alg(to_pos)}."

    def _play_ai_if_needed(self) -> Optional[str]:
        if not self.ai_enabled or self.board.to_move != "b":
            return None

        score, best = ai_engine.minimax(
            self.board,
            self.ai_depth,
            maximizing=False,
        )

        mv = best
        if mv is None:
            mv = ai_engine.greedy_move(self.board, "b")

        if mv is None:
            return "AI has no legal moves."

        frm, to = mv
        piece_moved = self.board.get_piece(frm)
        captured = self.board.get_piece(to)
        move_obj = Move(frm, to, piece_moved, captured)
        self.board.move_piece(frm, to)
        self.history.append(move_obj)
        self.undo_stack.push(move_obj)
        self.redo_stack.clear()
        self.played_moves.append(move_obj)

        # Track captured pieces
        if captured:
            captured_info = {
                "symbol": captured.symbol(),
                "color": captured.color,
                "type": captured.__class__.__name__,
            }
            if captured.color == "w":
                self.captured_white.append(captured_info)
            else:
                self.captured_black.append(captured_info)

        return f"AI played {self.pos_to_alg(frm)} to {self.pos_to_alg(to)} (score {score})."

    def do_move(self, from_square: str, to_square: str) -> Tuple[bool, str]:
        from_pos = self.alg_to_pos(from_square)
        to_pos = self.alg_to_pos(to_square)
        if from_pos is None or to_pos is None:
            return False, "Invalid coordinates. Use algebraic squares like e2 and e4."

        ok, message = self._apply_move(from_pos, to_pos)
        if not ok:
            return False, message

        ai_message = self._play_ai_if_needed()
        if ai_message:
            message = f"{message} {ai_message}"

        self.last_message = message
        return True, message

    def legal_targets(self, from_square: str) -> List[str]:
        from_pos = self.alg_to_pos(from_square)
        if from_pos is None:
            return []
        piece_obj = self.board.get_piece(from_pos)
        if piece_obj is None:
            return []
        if piece_obj.color != self.board.to_move:
            return []

        legal = self.board.generate_legal_moves(self.board.to_move)
        return [self.pos_to_alg(to_pos) for src, to_pos in legal if src == from_pos]

    def undo(self) -> Tuple[bool, str]:
        last = self.undo_stack.pop()
        if last is None:
            return False, "Nothing to undo."
        self.board.undo_move(last)
        self.redo_stack.push(last)
        if self.played_moves:
            self.played_moves.pop()

        # Remove captured piece from tracking if it exists
        if last.captured:
            if last.captured.color == "w":
                if self.captured_white:
                    self.captured_white.pop()
            else:
                if self.captured_black:
                    self.captured_black.pop()

        self.last_message = f"Undid {last}."
        return True, self.last_message

    def redo(self) -> Tuple[bool, str]:
        move_obj = self.redo_stack.pop()
        if move_obj is None:
            return False, "Nothing to redo."
        self.board.move_piece(move_obj.from_pos, move_obj.to_pos)
        self.undo_stack.push(move_obj)
        self.history.append(move_obj)
        self.played_moves.append(move_obj)
        self.last_message = f"Redid {move_obj}."
        return True, self.last_message

    def run_command(self, command: str) -> Tuple[bool, str]:
        parts = command.strip().split()
        if not parts:
            return False, "Empty command."

        cmd = parts[0].lower()

        if cmd == "help":
            return (
                True,
                "Commands: <from> <to>, undo, redo, history, ai on/off, ai depth <n>, reset",
            )

        if cmd == "undo":
            return self.undo()

        if cmd == "redo":
            return self.redo()

        if cmd == "history":
            if not self.played_moves:
                return True, "No moves yet."
            text = " | ".join(str(m) for m in self.played_moves)
            return True, text

        if cmd == "reset":
            self.reset()
            return True, "Game reset."

        if cmd == "ai":
            if len(parts) >= 2 and parts[1].lower() == "on":
                self.ai_enabled = True
                return True, "AI enabled for Black."
            if len(parts) >= 2 and parts[1].lower() == "off":
                self.ai_enabled = False
                return True, "AI disabled."
            if len(parts) >= 3 and parts[1].lower() == "depth":
                try:
                    depth = int(parts[2])
                except ValueError:
                    return False, "Invalid depth value."
                if depth < 1 or depth > 5:
                    return False, "Depth must be between 1 and 5."
                self.ai_depth = depth
                return True, f"AI depth set to {depth}."
            return False, "Invalid AI command. Use: ai on, ai off, ai depth <n>."

        if len(parts) >= 2:
            return self.do_move(parts[0], parts[1])

        return False, "Unknown command."

    def state_payload(self) -> Dict:
        legal_moves = self.board.generate_legal_moves(self.board.to_move)
        return {
            "board": self._board_payload(),
            "to_move": self.board.to_move,
            "status": self._status_text(),
            "ai_enabled": self.ai_enabled,
            "ai_depth": self.ai_depth,
            "last_message": self.last_message,
            "history": [str(m) for m in self.played_moves],
            "legal_move_count": len(legal_moves),
            "captured_white": self.captured_white,
            "captured_black": self.captured_black,
        }


app = FastAPI(title="Chess API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GAME = ChessGame()


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/state")
def get_state():
    return GAME.state_payload()


@app.get("/api/legal/{square}")
def get_legal(square: str):
    return {"from_square": square, "targets": GAME.legal_targets(square)}


@app.post("/api/move")
def post_move(payload: MoveRequest):
    ok, message = GAME.do_move(payload.from_square, payload.to_square)
    return {"ok": ok, "message": message, "state": GAME.state_payload()}


@app.post("/api/command")
def post_command(payload: CommandRequest):
    ok, message = GAME.run_command(payload.command)
    return {"ok": ok, "message": message, "state": GAME.state_payload()}


@app.post("/api/reset")
def post_reset():
    GAME.reset()
    return {"ok": True, "message": "Game reset.", "state": GAME.state_payload()}


@app.post("/api/undo")
def post_undo():
    ok, message = GAME.undo()
    return {"ok": ok, "message": message, "state": GAME.state_payload()}
