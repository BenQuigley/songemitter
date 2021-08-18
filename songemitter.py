"""Songwriting script."""
import sys
import logging
import random


logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)  # overwriteable by e.g. `-vv` in args

NOTES = ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
INTERVALS = (
    "same note",  # 0
    "half step",  # 1
    "whole step",  # 2
    "minor third",  # 3
    "major third",  # 4
    "fourth",  # 5
    "tritone",  # 6
    "fifth",  # 7
)
GUITAR_WEIGHTS = {
    # Not all guitar chords are equally ergonomic.
    "A":  1,
    "A#": .2,
    "B":  .2,
    "C":  1,
    "C#": .2,
    "D":  1,
    "D#": .2,
    "E":  1,
    "F":  .8,
    "F#": .2,
    "G":  1,
    "G#": .2,
}


def random_major_chord_guitar_weighted():
    return random.choices(
        tuple(GUITAR_WEIGHTS.keys()), weights=tuple(GUITAR_WEIGHTS.values())
    )[0]


def note_distance(note_a, note_b):
    """Return the relationship between two notes."""
    note_a = note_a.upper()
    note_b = note_b.upper()
    return (NOTES.index(note_b) - NOTES.index(note_a)) % 12


class Chord:
    """Python representation of an abstract chord."""

    forms = "major", "minor"

    def __init__(self, note, form):
        self.note = note
        self.form = form

def make_line(num_chords_per_line):
    return tuple(random_major_chord_guitar_weighted() for _ in range(num_chords_per_line))


def make_verse(num_lines_per_verse, num_chords_per_line):
    return tuple(make_line(num_chords_per_line) for _ in range(num_lines_per_verse))


def format_verse(lines, name="verse"):
    verse = [f"[{name}]\n"]
    for line in lines:
        verse.append(" - ".join((chord for chord in line)))
    return "\n".join(verse)


def main(verbosity=0):
    num_introductory_verses = random.randrange(0, 2)  # verses not followed by a chorus  # nosec
    num_lines_per_verse = 4
    num_chords_per_line = random.randrange(2, 5)  # nosec
    num_verses = random.randrange(max(4, num_introductory_verses), 6)  # nosec
    capo = random.choice((None, random.randrange(1, 7)))  # nosec
    verse = format_verse(make_verse(num_lines_per_verse, num_chords_per_line))
    chorus = format_verse(make_verse(num_lines_per_verse, num_chords_per_line), name="chorus")
    capo_note = f"Capo {capo}"
    song = [capo_note] if capo else []
    logger.debug(capo_note)
    logger.debug("%s chords per line", num_chords_per_line)
    logger.debug("%s lines per verse", num_lines_per_verse)
    print(f"{num_introductory_verses} introductory verses (verses not followed by a chorus)")
    print(f"{num_verses} verses total")
    if verbosity == 0:
        song.append(verse)
        song.append(chorus)
    else:
        for _ in range(num_introductory_verses):
            song.append(verse)
        for _ in range(num_introductory_verses, num_verses):
            song.append(verse)
            song.append(chorus)
    print("\n\n".join(song))


def quick_parse_args():
    """It's faster to write this than to look up the correct incantations of argparse"""
    usage = (
        "-h / --help: print usage\n"
        "-v: verbose\n"
        "-vv: very verbose\n"
    )
    parsed_args = {'verbosity': 0}   # defaults
    unrecognized_args = set()
    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            print(usage)
            sys.exit()
        elif set(arg) == {"-", "v"}:
            verbosity_options = (logging.WARNING, logging.INFO, logging.DEBUG)
            verbosity = min(arg.count("v"), len(verbosity_options)-1)
            parsed_args['verbosity'] = verbosity
            logger.setLevel(verbosity_options[verbosity])
        else:
            unrecognized_args.add(arg)
    if unrecognized_args:
        raise ValueError("Unrecognize args: {unrecognized_args}")
    return parsed_args


if __name__ == "__main__":
    args = quick_parse_args()
    main(**args)
