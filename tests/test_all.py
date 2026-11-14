"""Basic correctness tests (no external test framework required)."""

from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from structures.array_ops import FixedArray, DynamicArray
from structures.linked_lists import SinglyLinkedList, DoublyLinkedList
from structures.sqd import Stack, Queue, Deque
from structures.hash_table import HashTable
from structures.bst import BinarySearchTree
from apps.bracket_checker import is_balanced
from apps.ticket_line import process_line
from apps.music_playlist import Playlist


def check(name, condition):
    if not condition:
        raise AssertionError(f"FAIL: {name}")
    print(f"  OK  {name}")


def test_arrays():
    print("Arrays")
    fa = FixedArray(3)
    fa.append(1)
    fa.append(2)
    fa.insert(1, 9)
    check("fixed insert", fa.to_list() == [1, 9, 2])
    try:
        fa.append(4)
        check("fixed overflow", False)
    except OverflowError:
        check("fixed overflow", True)

    da = DynamicArray(2)
    for i in range(10):
        da.append(i)
    check("dynamic grew", len(da) == 10 and da.capacity >= 10)
    check("dynamic search", da.search(7) == 7)
    da.remove_at(0)
    check("dynamic remove", da.get(0) == 1)


def test_lists():
    print("Linked lists")
    s = SinglyLinkedList()
    s.insert_back(1)
    s.insert_front(0)
    s.insert_back(2)
    check("singly order", s.to_list() == [0, 1, 2])
    check("singly delete front", s.delete_front() == 0)

    d = DoublyLinkedList()
    d.insert_back("a")
    d.insert_back("b")
    d.insert_front("z")
    check("doubly order", d.to_list() == ["z", "a", "b"])
    check("doubly delete back", d.delete_back() == "b")


def test_sqd():
    print("Stack / Queue / Deque")
    st = Stack()
    st.push(1)
    st.push(2)
    check("stack peek", st.peek() == 2)
    check("stack pop", st.pop() == 2)

    q = Queue()
    q.enqueue("x")
    q.enqueue("y")
    check("queue front", q.front() == "x")
    check("queue dequeue", q.dequeue() == "x")

    dq = Deque()
    dq.add_back(1)
    dq.add_front(0)
    dq.add_back(2)
    check("deque list", dq.to_list() == [0, 1, 2])
    check("deque remove front", dq.remove_front() == 0)


def test_hash():
    print("Hash table")
    ht = HashTable(capacity=4)
    ht.put("name", "Said")
    ht.put("age", 20)
    ht.put("name", "Said A.")  # update
    check("hash get", ht.get("name") == "Said A.")
    check("hash contains", ht.contains("age"))
    ht.remove("age")
    check("hash remove", not ht.contains("age"))
    # Force collisions / resize
    for i in range(50):
        ht.put(i, i)
    check("hash size", len(ht) >= 50)


def test_bst():
    print("BST")
    tree = BinarySearchTree()
    for v in [5, 3, 7, 2, 4]:
        tree.insert(v)
    check("bst search", tree.search(4))
    check("bst missing", not tree.search(9))
    check("bst inorder", tree.inorder() == [2, 3, 4, 5, 7])
    check("bst height", tree.height() == 2)
    tree.delete(3)
    check("bst delete", tree.inorder() == [2, 4, 5, 7])

    # Balance problem: sorted inserts grow height linearly
    bad = BinarySearchTree()
    for i in range(20):
        bad.insert(i)
    check("bst sorted height high", bad.height() == 19)


def test_apps():
    print("Mini apps")
    check("brackets ok", is_balanced("{[()]}"))
    check("brackets bad", not is_balanced("(]"))
    served, _ = process_line(["A", "B", "C"])
    check("ticket fifo", served == ["A", "B", "C"])
    pl = Playlist()
    pl.add_last("B")
    pl.add_next("A")
    check("playlist", pl.show() == ["A", "B"])


def run_all():
    print("Running tests...")
    test_arrays()
    test_lists()
    test_sqd()
    test_hash()
    test_bst()
    test_apps()
    print("All tests passed.")


if __name__ == "__main__":
    run_all()
