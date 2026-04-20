"""main.py
Entry point for the terminal-based chess game demonstrating OOP and DSA.

Features implemented:
- Optional AI (greedy or minimax)
- Undo/Redo via Stack
- Move history via LinkedList
- Turn management via Queue
"""

from board import Board
from move import Move
from move_history import MoveLinkedList, Stack, TurnQueue
import ai_engine


def alg_to_pos(s: str):
    # e2 -> (6,4)
    try:
        file = s[0]
        rank = int(s[1])
        col = ord(file) - ord("a")
        row = 8 - rank
        return (row, col)
    except Exception:
        return None


def pos_to_alg(pos):
    r, c = pos
    return f"{chr(ord('a') + c)}{8 - r}"


def print_help():
    print("Commands:")
    print("  <from> <to>    e.g., e2 e4")
    print("  undo           undo last move")
    print("  redo           redo last undone move")
    print("  history        show move history")
    print("  ai on|off      toggle AI (black)")
    print("  ai depth <n>   set minimax depth")
    print("  quit           exit")


def main():
    b = Board()
    history = MoveLinkedList()  # Linked List storing move history
    undo_stack = Stack()  # Stack used to revert last moves
    redo_stack = Stack()
    turns = TurnQueue(["w", "b"])  # Queue for turn alternation

    ai_enabled = False
    ai_depth = 2

    print("Welcome to Python Chess (OOP + DSA Edition)")
    print_help()

    while True:
        print("\nCurrent board:")
        b.print_board()
        side = b.to_move
        print(f"{('White' if side=='w' else 'Black')} to move")

        # If AI is enabled and it's black's turn, have AI move
        if ai_enabled and side == "b":
            print("AI thinking...")
            score, mv = ai_engine.minimax(b, ai_depth, maximizing=(side == "w"))
            if mv is None:
                # fallback greedy
                gm = ai_engine.greedy_move(b, side)
                mv = gm
            if mv:
                frm, to = mv
                piece_moved = b.get_piece(frm)
                captured = b.get_piece(to)
                move_obj = Move(frm, to, piece_moved, captured)
                b.move_piece(frm, to)
                history.append(move_obj)
                undo_stack.push(move_obj)
                redo_stack.clear()
                continue
            else:
                print("AI had no legal moves.")

        cmd = input("Enter move (e.g., e2 e4) or command: ").strip()
        if not cmd:
            continue
        parts = cmd.split()
        if parts[0] == "quit":
            break
        if parts[0] == "help":
            print_help()
            continue
        if parts[0] == "undo":
            last = undo_stack.pop()
            if last:
                b.undo_move(last)
                redo_stack.push(last)
                print(f"Undid {last}")
            else:
                print("Nothing to undo")
            continue
        if parts[0] == "redo":
            itm = redo_stack.pop()
            if itm:
                b.move_piece(itm.from_pos, itm.to_pos)
                undo_stack.push(itm)
                history.append(itm)
                print(f"Redid {itm}")
            else:
                print("Nothing to redo")
            continue
        if parts[0] == "history":
            for i, mv in enumerate(history):
                print(f"{i+1}. {mv}")
            continue
        if parts[0] == "ai":
            if len(parts) >= 2 and parts[1] == "on":
                ai_enabled = True
                print("AI enabled for Black")
            elif len(parts) >= 2 and parts[1] == "off":
                ai_enabled = False
                print("AI disabled")
            elif len(parts) >= 3 and parts[1] == "depth":
                try:
                    ai_depth = int(parts[2])
                    print(f"AI depth set to {ai_depth}")
                except ValueError:
                    print("Invalid depth")
            else:
                print_help()
            continue

        # Parse move
        if len(parts) >= 2:
            a = alg_to_pos(parts[0])
            bpos = alg_to_pos(parts[1])
            if a is None or bpos is None:
                print("Invalid coordinates. Use format like e2 e4")
                continue
            piece_obj = b.get_piece(a)
            if piece_obj is None:
                print("No piece at source square")
                continue
            if piece_obj.color != side:
                print("You must move your own piece")
                continue

            legal = b.generate_legal_moves(side)
            if (a, bpos) in legal:
                captured = b.get_piece(bpos)
                move_obj = Move(a, bpos, piece_obj, captured)
                b.move_piece(a, bpos)
                history.append(move_obj)
                undo_stack.push(move_obj)
                redo_stack.clear()
            else:
                print("Illegal move")
            continue

        print("Unknown command. Type 'help' for commands.")


if __name__ == "__main__":
    main()
