"""move_history.py
Implements LinkedList for move history, Stack for undo/redo, and Queue for turn management.

DSA Concepts :
- Linked List: doubly-linked list to store moves for easy traversal/backtracking.
  # Linked List used to store move history with easy undo traversal.
- Stack: LIFO used for undo and redo stacks.
  # Stack used to revert the last move efficiently.
- Queue: FIFO used to manage player turns.
  # Queue used to manage alternating player turns.
"""

from collections import deque
from typing import Optional
from move import Move


class Node:
    def __init__(self, move: Move):
        self.move = move
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class MoveLinkedList:
    """Doubly-linked list storing moves in chronological order."""

    def __init__(self):
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None
        self.size = 0

    def append(self, move: Move):
        node = Node(move)
        if not self.head:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
        self.size += 1

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.move
            cur = cur.next

    def last(self) -> Optional[Move]:
        return self.tail.move if self.tail else None


class Stack:
    """Simple Stack wrapper around list for LIFO operations."""

    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self._data:
            return self._data.pop()
        return None

    def peek(self):
        return self._data[-1] if self._data else None

    def is_empty(self):
        return len(self._data) == 0

    def clear(self):
        self._data.clear()


class TurnQueue:
    """Queue to manage turn order. For two players it's a trivial alternator.

    Demonstrates FIFO queue usage.
    """

    def __init__(self, items=None):
        self._q = deque(items if items else [])

    def enqueue(self, item):
        self._q.append(item)

    def dequeue(self):
        return self._q.popleft() if self._q else None

    def peek(self):
        return self._q[0] if self._q else None

    def rotate(self):
        # move front to back (used to alternate turns)
        if self._q:
            self._q.append(self._q.popleft())

    def __len__(self):
        return len(self._q)
