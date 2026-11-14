"""Mini-app: check balanced brackets using a Stack."""

from structures.sqd import Stack


PAIRS = {")": "(", "]": "[", "}": "{"}


def is_balanced(text):
    """Return True if (), [], {} are correctly nested."""
    stack = Stack()
    for ch in text:
        if ch in "([{":
            stack.push(ch)
        elif ch in ")]}":
            if stack.is_empty():
                return False
            if stack.pop() != PAIRS[ch]:
                return False
    return stack.is_empty()


def demo():
    samples = [
        "()[]{}",
        "(]",
        "{[()]}",
        "(((",
        "a+(b*[c-d])",
    ]
    print("=== Bracket Checker (Stack) ===")
    for s in samples:
        status = "BALANCED" if is_balanced(s) else "NOT balanced"
        print(f"  {s!r:20} -> {status}")
