"""Simple performance benchmarks using time.perf_counter.

Writes a text/CSV-like report under results/.
"""

from __future__ import annotations

import os
import random
import sys
import time

# Allow running as: python benchmarks/run_benchmarks.py
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from structures.array_ops import FixedArray, DynamicArray
from structures.linked_lists import SinglyLinkedList, DoublyLinkedList
from structures.hash_table import HashTable
from structures.bst import BinarySearchTree


SIZES = [100, 1000, 5000]


def ns(fn):
    start = time.perf_counter_ns()
    fn()
    return time.perf_counter_ns() - start


def us(nanoseconds):
    return nanoseconds / 1000.0


def bench_arrays(lines):
    lines.append("## Array vs Dynamic Array")
    lines.append("size,structure,op,microseconds")
    for n in SIZES:
        # FixedArray append (capacity = n so it never overflows)
        fixed = FixedArray(n)

        def fixed_append():
            for i in range(n):
                fixed.append(i)

        t = ns(fixed_append)
        lines.append(f"{n},FixedArray,append,{us(t):.2f}")

        dyn = DynamicArray(4)

        def dyn_append():
            for i in range(n):
                dyn.append(i)

        t = ns(dyn_append)
        lines.append(f"{n},DynamicArray,append,{us(t):.2f}")

        # Mid insert on DynamicArray of size n/2 then one insert
        dyn2 = DynamicArray()
        for i in range(n):
            dyn2.append(i)
        mid = n // 2
        t = ns(lambda: dyn2.insert(mid, -1))
        lines.append(f"{n},DynamicArray,insert_middle,{us(t):.2f}")

        # Search last element
        target = n - 1
        t = ns(lambda: dyn2.search(target))
        lines.append(f"{n},DynamicArray,search,{us(t):.2f}")
    lines.append("")


def bench_lists(lines):
    lines.append("## Singly vs Doubly Linked List")
    lines.append("size,structure,op,microseconds")
    for n in SIZES:
        s = SinglyLinkedList()
        t = ns(lambda: [s.insert_front(i) for i in range(n)])
        lines.append(f"{n},Singly,insert_front,{us(t):.2f}")

        s2 = SinglyLinkedList()
        t = ns(lambda: [s2.insert_back(i) for i in range(n)])
        lines.append(f"{n},Singly,insert_back,{us(t):.2f}")

        d = DoublyLinkedList()
        t = ns(lambda: [d.insert_front(i) for i in range(n)])
        lines.append(f"{n},Doubly,insert_front,{us(t):.2f}")

        d2 = DoublyLinkedList()
        t = ns(lambda: [d2.insert_back(i) for i in range(n)])
        lines.append(f"{n},Doubly,insert_back,{us(t):.2f}")
    lines.append("")


def bench_hash(lines):
    lines.append("## Hash Table vs Linear List Search")
    lines.append("size,structure,op,microseconds")
    for n in SIZES:
        ht = HashTable()
        keys = list(range(n))

        def ht_put():
            for k in keys:
                ht.put(k, k * 2)

        t = ns(ht_put)
        lines.append(f"{n},HashTable,put,{us(t):.2f}")

        target = n - 1
        t = ns(lambda: ht.get(target))
        lines.append(f"{n},HashTable,get,{us(t):.2f}")

        arr = list(range(n))

        def linear():
            return target in arr

        t = ns(linear)
        lines.append(f"{n},List,linear_search,{us(t):.2f}")

        # Force collisions: many keys into a tiny table (disable resize).
        tiny = HashTable(capacity=8)
        tiny._load_factor_threshold = float("inf")
        for k in range(min(n, 200)):
            tiny.put(f"key-{k}", k)
        lines.append(f"{n},HashTable,collision_buckets_cap8,{tiny.collision_count()}")
    lines.append("")


def bench_bst(lines):
    lines.append("## BST: random vs sorted insertion (balance problem)")
    lines.append("size,order,height,search_microseconds")
    for n in SIZES:
        # Sorted -> degenerate (linked-list like) tree
        sorted_tree = BinarySearchTree()
        for i in range(n):
            sorted_tree.insert(i)
        t = ns(lambda: sorted_tree.search(n - 1))
        lines.append(f"{n},sorted,{sorted_tree.height()},{us(t):.2f}")

        # Random -> usually more balanced
        random_tree = BinarySearchTree()
        values = list(range(n))
        random.seed(42)
        random.shuffle(values)
        for v in values:
            random_tree.insert(v)
        t = ns(lambda: random_tree.search(n - 1))
        lines.append(f"{n},random,{random_tree.height()},{us(t):.2f}")
    lines.append("")


def run_all(save=True):
    lines = [
        "# Benchmark results",
        f"# sizes={SIZES}",
        "# times are approximate (microseconds); machine-dependent",
        "",
    ]
    bench_arrays(lines)
    bench_lists(lines)
    bench_hash(lines)
    bench_bst(lines)

    text = "\n".join(lines)
    print(text)

    if save:
        out_dir = os.path.join(ROOT, "results")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "benchmark_results.txt")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved to {out_path}")
    return text


if __name__ == "__main__":
    run_all(save=True)
