NOTES = ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
INTERVALS = (
    "same note",    # 0
    "half step",    # 1
    "whole step",   # 2
    "minor third",  # 3
    "major third",  # 4
    "fourth",       # 5
    "tritone",      # 6
    "fifth",        # 7
)


def note_distance(note_a, note_b):
    """Return the relationship between two notes."""
    note_a = note_a.upper()
    note_b = note_b.upper()
    return (NOTES.index(note_b) - NOTES.index(note_a)) % 12

class Chord:
    """Python representation of an abstract chord."""
