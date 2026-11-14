"""Mini-app: ticket / customer line using a Queue (FIFO)."""

from structures.sqd import Queue


def process_line(names):
    """Enqueue all names, then serve them in arrival order."""
    line = Queue()
    log = []
    for name in names:
        line.enqueue(name)
        log.append(f"joined: {name} (line size={len(line)})")
    served = []
    while not line.is_empty():
        person = line.dequeue()
        served.append(person)
        log.append(f"served: {person}")
    return served, log


def demo():
    customers = ["Aysel", "Rauf", "Leyla", "Kamran", "Nigar"]
    served, log = process_line(customers)
    print("=== Ticket Line (Queue) ===")
    for entry in log:
        print(" ", entry)
    print(" Order served:", " -> ".join(served))
