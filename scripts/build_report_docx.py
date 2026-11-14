"""Build a Word technical report for our DSA team project.

Structure mirrors a typical lab report (intro → architecture → why →
complexity → tests → benchmarks → analysis → trade-offs), but all content,
apps, paths and numbers are specific to this repository.
"""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "DSA_Serbest_Is_Hesabat.docx"


def set_cell_shading(cell, hex_color: str):
    shading = OxmlElement("w:shd")
    shading.set(qn("w:fill"), hex_color)
    shading.set(qn("w:val"), "clear")
    cell._tePr = cell._tc.get_or_add_tcPr()
    cell._tc.get_or_add_tcPr().append(shading)


def style_doc(doc: Document):
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style._element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")

    for i in range(1, 4):
        h = doc.styles[f"Heading {i}"]
        h.font.color.rgb = RGBColor(0x0B, 0x2A, 0x3A)
        h.font.name = "Calibri"


def add_heading(doc, text, level=1):
    return doc.add_heading(text, level=level)


def add_para(doc, text, bold=False):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    return p


def add_bullets(doc, items):
    for item in items:
        doc.add_paragraph(item, style="List Bullet")


def add_table(doc, headers, rows, header_color="0B2A3A"):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = h
        for p in hdr[i].paragraphs:
            for r in p.runs:
                r.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                r.font.size = Pt(9)
        set_cell_shading(hdr[i], header_color)
    for r_i, row in enumerate(rows):
        cells = table.rows[r_i + 1].cells
        for c_i, val in enumerate(row):
            cells[c_i].text = str(val)
            for p in cells[c_i].paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
            if r_i % 2 == 1:
                set_cell_shading(cells[c_i], "E6F3F0")
    doc.add_paragraph()
    return table


def build():
    doc = Document()
    style_doc(doc)
    for section in doc.sections:
        section.top_margin = Cm(2)
        section.bottom_margin = Cm(2)
        section.left_margin = Cm(2.2)
        section.right_margin = Cm(2.2)

    # Title
    t = doc.add_paragraph()
    t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = t.add_run(
        "Data Structures Lab Project:\n"
        "Custom Structures, Mini-Apps and Performance Benchmarks"
    )
    run.bold = True
    run.font.size = Pt(18)
    run.font.color.rgb = RGBColor(0x0B, 0x2A, 0x3A)

    add_para(
        doc,
        "Course: Müasir Data Strukturları və Alqoritmlər | "
        "Azerbaijan Technical University",
    )
    add_para(
        doc,
        "Team: Səid Abdullayev, Nicat İbrahimov, Yunus Həşimov",
    )
    add_para(doc, "Repository: https://github.com/Abdullaeff1/dsa-serbest-is")
    add_para(doc, "Topics covered: 1–5 (Array, Linked List, Stack/Queue/Deque, Hash Table, BST)")

    # 1
    add_heading(doc, "1. Introduction", 2)
    add_para(
        doc,
        "This project is a Python console application that implements five "
        "groups of data structures from scratch and measures how they behave "
        "on 100, 1,000 and 5,000 elements. The structures are: fixed and "
        "dynamic arrays; singly and doubly linked lists; stack, queue and "
        "deque; a hash table with separate chaining; and a binary search tree (BST).",
    )
    add_para(doc, "The goals were to:")
    add_bullets(
        doc,
        [
            "implement every structure ourselves (learning-focused, clear code);",
            "compare insertion, deletion and search with real timings;",
            "use Stack, Queue and Deque inside small application features;",
            "show how sorted input changes the shape and search cost of a BST;",
            "explain in writing why each structure fits its mini-app.",
        ],
    )
    add_para(
        doc,
        "Benchmark results are linked to theoretical complexity, and trade-offs "
        "are discussed at the end.",
    )

    # 2
    add_heading(doc, "2. Application and Architecture", 2)
    add_para(
        doc,
        "The application is a text menu (main.py). The user picks an option; "
        "the program runs demos, mini-apps, benchmarks or tests.",
    )
    add_para(doc, "Menu overview:", bold=True)
    add_table(
        doc,
        ["Menu option", "What it does"],
        [
            ["1", "Fixed / Dynamic Array demo"],
            ["2", "Singly / Doubly Linked List demo"],
            ["3", "Stack / Queue / Deque basics"],
            ["4", "Hash Table (chaining) demo"],
            ["5", "BST + balance tip (sorted vs mixed)"],
            ["6", "Mini-app: Bracket Checker (Stack)"],
            ["7", "Mini-app: Ticket Line (Queue)"],
            ["8", "Mini-app: Music Playlist (Deque)"],
            ["9", "Run benchmarks → results/benchmark_results.txt"],
            ["10", "Run automated tests"],
            ["0", "Exit"],
        ],
    )

    add_para(doc, "Project layout:", bold=True)
    add_table(
        doc,
        ["Path", "Content"],
        [
            ["main.py", "Interactive console menu"],
            ["structures/array_ops.py", "FixedArray, DynamicArray"],
            ["structures/linked_lists.py", "SinglyLinkedList, DoublyLinkedList"],
            ["structures/sqd.py", "Stack, Queue, Deque"],
            ["structures/hash_table.py", "HashTable with chaining"],
            ["structures/bst.py", "BinarySearchTree"],
            ["apps/", "Bracket / Ticket / Playlist mini-apps"],
            ["benchmarks/run_benchmarks.py", "Timing experiments"],
            ["tests/test_all.py", "Correctness checks"],
            ["docs/", "Presentation, PDF and this report"],
        ],
    )
    add_para(
        doc,
        "Setup and run: Python 3.10+ (no external packages required for the app). "
        "In the project folder run: python main.py  |  python tests/test_all.py  |  "
        "python benchmarks/run_benchmarks.py",
    )
    add_para(
        doc,
        "Structures build on each other: Stack uses DynamicArray; Queue and Deque "
        "use DoublyLinkedList so end operations stay O(1).",
    )

    # 3
    add_heading(doc, "3. Data Structures and Why We Chose Them", 2)
    paragraphs = [
        (
            "Fixed array. ",
            "A fixed block of slots with a size counter. Index access is O(1). "
            "Insert/delete in the middle shifts elements. It cannot grow, so it "
            "is the baseline for comparison with the dynamic array.",
        ),
        (
            "Dynamic array. ",
            "Doubles capacity when full and halves when size falls to about 1/4. "
            "Append is amortized O(1). We use it as the base of the Stack because "
            "push/pop happen at one end.",
        ),
        (
            "Singly linked list. ",
            "Nodes with only next, and a head pointer. Front insert/delete are O(1); "
            "back operations walk the list O(n). Kept head-only on purpose to contrast "
            "with the doubly linked list.",
        ),
        (
            "Doubly linked list. ",
            "prev/next plus head and tail. Both ends are O(1). Extra memory per node. "
            "Chosen as the base of Queue and Deque.",
        ),
        (
            "Stack → Bracket Checker. ",
            "Last opened bracket must close first (LIFO). Push opening symbols, "
            "pop on closing symbols and check the pair. This is the natural model "
            "for nested matching.",
        ),
        (
            "Queue → Ticket Line. ",
            "Customers must be served in arrival order (FIFO). Enqueue at the back, "
            "dequeue from the front. A doubly linked list keeps both ends O(1).",
        ),
        (
            "Deque → Music Playlist. ",
            "Songs may be added at the front (play sooner) or at the back. "
            "Deque supports O(1) updates at both ends.",
        ),
        (
            "Hash table (chaining). ",
            "Key → bucket index via hash; each bucket is a list of (key, value) pairs. "
            "Collisions share a chain. When load factor exceeds ~0.75 the table "
            "doubles and rehashes. Chosen for average O(1) key lookup.",
        ),
        (
            "Binary search tree. ",
            "Left < node < right. Search/insert/delete depend on height h. "
            "Height is computed iteratively so a tall sorted tree does not hit "
            "Python’s recursion limit. Sorted inserts demonstrate the balance problem.",
        ),
    ]
    for bold, rest in paragraphs:
        p = doc.add_paragraph()
        r = p.add_run(bold)
        r.bold = True
        p.add_run(rest)

    # 4
    add_heading(doc, "4. Complexity Analysis (Time and Space)", 2)
    add_para(
        doc,
        "n is the number of stored elements. An asterisk (*) marks amortized cost.",
    )
    add_table(
        doc,
        ["Structure", "Access", "Search", "Insert", "Delete", "Space"],
        [
            ["Fixed Array", "O(1)", "O(n)", "O(1) end / O(n) else", "O(1) end / O(n) else", "O(capacity)"],
            ["Dynamic Array", "O(1)", "O(n)", "O(1)* end / O(n)", "O(n)", "O(capacity)"],
            ["Singly LL", "O(n)", "O(n)", "O(1) front / O(n) back", "O(1) front / O(n) back", "O(n)"],
            ["Doubly LL", "O(n)", "O(n)", "O(1) both ends", "O(1) both ends", "O(n)"],
            ["Stack", "—", "—", "push O(1)*", "pop O(1)*", "O(n)"],
            ["Queue", "—", "—", "enqueue O(1)", "dequeue O(1)", "O(n)"],
            ["Deque", "—", "—", "O(1) both ends", "O(1) both ends", "O(n)"],
            ["Hash (chaining)", "—", "avg O(1) / worst O(n)", "avg O(1)", "avg O(1)", "O(n)"],
            ["BST random", "—", "avg O(log n)", "avg O(log n)", "avg O(log n)", "O(n)"],
            ["BST sorted", "—", "O(n)", "O(n)", "O(n)", "O(n)"],
        ],
    )
    add_para(doc, "Space notes:", bold=True)
    add_bullets(
        doc,
        [
            "All structures store n items → space is O(n); constants differ.",
            "Dynamic array keeps spare capacity because of doubling.",
            "Singly nodes store one pointer; doubly nodes store two.",
            "Hash table stores bucket array + chain entries.",
            "BST shape does not change total node count, but it decides speed.",
        ],
    )

    # 5
    add_heading(doc, "5. Test Scenarios", 2)
    add_para(
        doc,
        "tests/test_all.py runs automatic checks and prints OK / FAIL. "
        "All checks pass on our machine.",
    )
    add_table(
        doc,
        ["Structure", "Scenario", "Expected result"],
        [
            ["FixedArray", "Insert then append when full", "Order kept; OverflowError when full"],
            ["DynamicArray", "Append past initial capacity", "Capacity grows; values preserved"],
            ["Singly LL", "insert_front / insert_back / delete_front", "Correct order"],
            ["Doubly LL", "insert ends + delete_back", "Head/tail stay consistent"],
            ["Stack", "push then pop", "LIFO order"],
            ["Queue", "enqueue then dequeue", "FIFO order"],
            ["Deque", "add_front / add_back", "Correct sequence"],
            ["HashTable", "put, update, remove, many inserts", "Values correct after resize"],
            ["BST", "inorder, delete, sorted insert height", "Sorted inorder; tall sorted tree"],
            ["Apps", "brackets / ticket / playlist", "Balanced check, FIFO serve, front insert"],
        ],
    )

    # 6
    add_heading(doc, "6. Benchmark Method and Test Inputs", 2)
    add_para(doc, "Sizes. Benchmarks use n = 100, 1,000 and 5,000.")
    add_para(doc, "Test inputs.", bold=True)
    add_table(
        doc,
        ["Benchmark", "Input"],
        [
            ["Arrays", "Integers 0..n-1 appended; mid insert; search last value"],
            ["Linked lists", "n insert_front and n insert_back timings (total build)"],
            ["Hash table", "put keys 0..n-1; get last key; linear list search for comparison"],
            ["Hash collisions demo", "capacity fixed at 8 (resize disabled) with string keys"],
            ["BST", "insert 0..n-1 sorted; insert shuffled with seed=42; search n-1"],
        ],
    )
    add_para(doc, "Timing.", bold=True)
    add_bullets(
        doc,
        [
            "Clock: time.perf_counter_ns.",
            "Build-style operations measure the total work for n calls.",
            "Results are reported in microseconds (µs).",
            "Absolute times depend on the machine; growth trends matter more.",
        ],
    )
    add_para(
        doc,
        "Machine: Intel (Family 6 Model 186), Windows 11, Python 3.12.10. "
        "Source file: results/benchmark_results.txt (menu option 9 / run_benchmarks.py).",
    )

    # 7
    add_heading(doc, "7. Benchmark Results", 2)
    add_para(doc, "All times are in microseconds unless noted.")

    add_heading(doc, "7.1 Array and Dynamic Array", 3)
    add_table(
        doc,
        ["n", "Fixed append (total)", "Dynamic append (total)", "Insert middle", "Search"],
        [
            ["100", "21.60", "42.00", "5.80", "5.40"],
            ["1,000", "168.20", "199.20", "33.70", "45.30"],
            ["5,000", "818.40", "1,059.60", "148.30", "207.60"],
        ],
    )

    add_heading(doc, "7.2 Singly vs Doubly Linked List (total for n inserts)", 3)
    add_table(
        doc,
        ["n", "Singly front", "Singly back", "Doubly front", "Doubly back"],
        [
            ["100", "105.90", "265.90", "207.80", "62.80"],
            ["1,000", "620.00", "9,075.90", "319.60", "816.10"],
            ["5,000", "1,294.70", "223,014.30", "1,479.50", "1,419.60"],
        ],
    )

    add_heading(doc, "7.3 Hash table vs linear list search", 3)
    add_table(
        doc,
        ["n", "Hash put (total)", "Hash get", "List linear search", "Collision buckets (cap=8 demo)"],
        [
            ["100", "174.10", "2.00", "1.30", "8"],
            ["1,000", "1,248.60", "2.20", "5.50", "8"],
            ["5,000", "5,770.00", "1.50", "24.40", "8"],
        ],
    )
    add_para(
        doc,
        "Note: with capacity fixed at 8 and resize disabled, all 8 buckets hold "
        "colliding chains — this is a deliberate collision demonstration, not the "
        "normal resized table.",
    )

    add_heading(doc, "7.4 BST: random order against sorted order", 3)
    add_table(
        doc,
        ["n", "Sorted height", "Random height", "Sorted search (µs)", "Random search (µs)"],
        [
            ["100", "99", "10", "5.40", "0.90"],
            ["1,000", "999", "20", "38.20", "2.00"],
            ["5,000", "4,999", "28", "184.30", "1.30"],
        ],
    )
    add_para(
        doc,
        "Best possible height for a perfectly balanced tree is about floor(log2 n): "
        "6 / 9 / 12 for these sizes. Our random trees are higher than ideal but "
        "still far below the sorted chain.",
    )

    # 8
    add_heading(doc, "8. Analysis of Results", 2)

    add_heading(doc, "8.1 Arrays", 3)
    add_bullets(
        doc,
        [
            "Dynamic append stays in the same order of magnitude as Fixed append "
            "(amortized O(1)), paying a modest constant for resizing checks/copies.",
            "Middle insert and search grow with n (~O(n)), matching theory.",
            "FixedArray cannot accept more than its capacity — useful teaching contrast.",
        ],
    )

    add_heading(doc, "8.2 Linked lists", 3)
    add_bullets(
        doc,
        [
            "At n = 5,000, Singly insert_back (~223 ms total) is roughly 150× slower "
            "than Doubly insert_back (~1.4 ms total), because Singly walks the whole list.",
            "Front inserts stay relatively cheap for both lists.",
            "This is exactly why Queue/Deque sit on the doubly linked list.",
        ],
    )

    add_heading(doc, "8.3 Hash table", 3)
    add_bullets(
        doc,
        [
            "After the table is built, get stays near-constant (~1.5–2.2 µs) while "
            "linear search grows with n (1.3 → 24.4 µs in our run).",
            "Building the table costs more than a plain append (hashing + buckets + resize).",
            "Chaining keeps collisions manageable; forced tiny capacity shows full-bucket chains.",
        ],
    )

    add_heading(doc, "8.4 Binary search tree", 3)
    add_bullets(
        doc,
        [
            "Random insert heights: 10 / 20 / 28 — search stays near 1–2 µs.",
            "Sorted insert heights: 99 / 999 / 4999 — the tree is a right spine (like a list).",
            "Sorted search at n = 5,000 (~184 µs) is about 140× slower than random (~1.3 µs).",
            "Why: each new key is larger than all previous keys, so insert walks the full chain; "
            "building becomes ~n²/2 pointer steps.",
            "Fixes: shuffle before insert, use AVL/Red-Black, or build from sorted data by "
            "recursively inserting the middle key.",
        ],
    )

    # 9
    add_heading(doc, "9. Trade-offs", 2)
    add_bullets(
        doc,
        [
            "Array vs linked list: arrays win on index access; lists win on end updates "
            "when the right end pointers exist.",
            "Fixed vs dynamic array: fixed uses exact capacity but cannot grow; dynamic "
            "grows on demand with spare slots.",
            "Singly vs doubly: singly saves a pointer; doubly makes both ends O(1).",
            "Stack / Queue / Deque: choose by behaviour (LIFO / FIFO / both ends), then "
            "pick a base that keeps the hot end O(1).",
            "Hash table: fastest average key lookup, but no order and needs a good hash / load factor.",
            "BST: keeps order (inorder = sorted) but speed depends on shape; sorted input "
            "destroys balance unless the tree self-balances.",
        ],
    )

    # 10
    add_heading(doc, "10. Team Contributions", 2)
    add_table(
        doc,
        ["Member", "Main contributions"],
        [
            ["Səid Abdullayev", "Array / Dynamic Array, Hash Table, main menu, tests"],
            ["Nicat İbrahimov", "Linked lists, Stack/Queue/Deque, mini-apps"],
            ["Yunus Həşimov", "BST + balance analysis, benchmarks, documentation"],
        ],
    )
    add_para(
        doc,
        "Individual work is visible in Git history (git shortlog -sn / git log --format).",
    )

    # 11
    add_heading(doc, "11. Conclusion", 2)
    add_para(
        doc,
        "The project covers topics 1–5 required by the assignment: custom implementations, "
        "mini-apps for Stack/Queue/Deque, chaining hash table, BST balance demonstration, "
        "complexity discussion and experimental benchmarks. Structure choices are tied to "
        "application needs, and the measurements match the expected Big-O trends.",
    )

    add_heading(doc, "12. References", 2)
    add_bullets(
        doc,
        [
            "Goodrich, Tamassia, Goldwasser — Data Structures and Algorithms in Python",
            "Cormen et al. — Introduction to Algorithms (hashing, BST chapters)",
            "Course syllabus — Müasir Data Strukturları və Alqoritmlər (topics 1–5)",
            "Project repository — https://github.com/Abdullaeff1/dsa-serbest-is",
        ],
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT)
    print("Wrote", OUT)
    return OUT


if __name__ == "__main__":
    build()
