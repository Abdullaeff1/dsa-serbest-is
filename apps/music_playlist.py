"""Mini-app: music playlist using a Deque (add/remove at both ends)."""

from structures.sqd import Deque


class Playlist:
    def __init__(self):
        self._tracks = Deque()

    def add_next(self, title):
        """Put song at the front (plays sooner)."""
        self._tracks.add_front(title)

    def add_last(self, title):
        """Put song at the end of the playlist."""
        self._tracks.add_back(title)

    def play_next(self):
        if self._tracks.is_empty():
            return None
        return self._tracks.remove_front()

    def remove_last(self):
        if self._tracks.is_empty():
            return None
        return self._tracks.remove_back()

    def show(self):
        return self._tracks.to_list()


def demo():
    pl = Playlist()
    pl.add_last("Song A")
    pl.add_last("Song B")
    pl.add_next("Intro")  # jumps to front
    pl.add_last("Song C")
    print("=== Music Playlist (Deque) ===")
    print(" Playlist now:", pl.show())
    print(" Playing:", pl.play_next())
    print(" After play:", pl.show())
    print(" Removed last:", pl.remove_last())
    print(" Final:", pl.show())
