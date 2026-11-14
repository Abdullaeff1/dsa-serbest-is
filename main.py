"""Interactive console menu for the DSA free-work project (topics 1-5)."""

from __future__ import annotations

import sys

from structures.array_ops import FixedArray, DynamicArray
from structures.linked_lists import SinglyLinkedList, DoublyLinkedList
from structures.sqd import Stack, Queue, Deque
from structures.hash_table import HashTable
from structures.bst import BinarySearchTree
from apps.bracket_checker import demo as demo_brackets
from apps.ticket_line import demo as demo_tickets
from apps.music_playlist import demo as demo_playlist
from benchmarks.run_benchmarks import run_all as run_benchmarks
from tests.test_all import run_all as run_tests


def demo_arrays():
    print("=== Fixed vs Dynamic Array ===")
    fixed = FixedArray(4)
    for x in [10, 20, 30]:
        fixed.append(x)
    print(" FixedArray:", fixed.to_list(), f"capacity={fixed.capacity}")

    dyn = DynamicArray(2)
    for x in range(6):
        dyn.append(x)
    print(" DynamicArray:", dyn.to_list(), f"capacity={dyn.capacity} (grew by doubling)")


def demo_lists():
    print("=== Singly vs Doubly Linked List ===")
    s = SinglyLinkedList()
    s.insert_back(1)
    s.insert_back(2)
    s.insert_front(0)
    print(" Singly:", s.to_list())

    d = DoublyLinkedList()
    d.insert_back("a")
    d.insert_back("b")
    d.insert_front("z")
    print(" Doubly:", d.to_list())
    print(" Note: Doubly insert_back is O(1); Singly insert_back is O(n).")


def demo_sqd_basic():
    print("=== Stack / Queue / Deque basics ===")
    st = Stack()
    for v in [1, 2, 3]:
        st.push(v)
    print(" Stack pop order:", st.pop(), st.pop(), st.pop())

    q = Queue()
    for v in ["A", "B", "C"]:
        q.enqueue(v)
    print(" Queue dequeue order:", q.dequeue(), q.dequeue(), q.dequeue())

    dq = Deque()
    dq.add_back(2)
    dq.add_front(1)
    dq.add_back(3)
    print(" Deque contents:", dq.to_list())


def demo_hash():
    print("=== Hash Table (chaining) ===")
    ht = HashTable(capacity=4)
    ht.put("CS101", "Alqoritmlər")
    ht.put("CS102", "Data strukturları")
    ht.put("MATH", "Diskret riyaziyyat")
    print(" get CS101:", ht.get("CS101"))
    print(" size:", len(ht), "| buckets with collisions:", ht.collision_count())


def demo_bst():
    print("=== Binary Search Tree + balance tip ===")
    random_like = BinarySearchTree()
    for v in [8, 3, 10, 1, 6, 14]:
        random_like.insert(v)
    print(" Mixed insert inorder:", random_like.inorder(), "height=", random_like.height())

    sorted_tree = BinarySearchTree()
    for v in range(1, 7):
        sorted_tree.insert(v)
    print(" Sorted insert inorder:", sorted_tree.inorder(), "height=", sorted_tree.height())
    print(" Sorted inserts make a tall (unbalanced) tree — search becomes slower.")


def print_menu():
    print(
        """
========================================
  Müasir Data Strukturları — Sərbəst İş
  Mövzular 1-5 | Konsol menyusu
========================================
  1) Array / Dynamic Array demo
  2) Singly / Doubly Linked List demo
  3) Stack / Queue / Deque demo
  4) Hash Table demo
  5) BST + balans demo
  6) Mini-tətbiq: Bracket Checker (Stack)
  7) Mini-tətbiq: Ticket Line (Queue)
  8) Mini-tətbiq: Music Playlist (Deque)
  9) Benchmark-ları işə sal
 10) Testləri işə sal
  0) Çıxış
"""
    )


def main():
    actions = {
        "1": demo_arrays,
        "2": demo_lists,
        "3": demo_sqd_basic,
        "4": demo_hash,
        "5": demo_bst,
        "6": demo_brackets,
        "7": demo_tickets,
        "8": demo_playlist,
        "9": lambda: run_benchmarks(save=True),
        "10": run_tests,
    }
    while True:
        print_menu()
        choice = input("Seçim: ").strip()
        if choice == "0":
            print("Sağolun!")
            break
        action = actions.get(choice)
        if action is None:
            print("Yanlış seçim.")
            continue
        print()
        action()
        print()
        input("Davam etmək üçün Enter...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDayandırıldı.")
        sys.exit(0)
