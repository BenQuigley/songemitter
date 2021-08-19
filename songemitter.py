"""Songwriting script."""
import json
import logging
import random
import sys
from dataclasses import dataclass
from typing import List, Optional

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.WARNING)  # overwriteable by e.g. `-vv` in args

NOTES = ("A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#")
GUITAR_WEIGHTS = {
    # Not all guitar chords are equally ergonomic.
    "A": 1,
    "A#": 0.2,
    "B": 0.2,
    "C": 1,
    "C#": 0.2,
    "D": 1,
    "D#": 0.2,
    "E": 1,
    "F": 0.8,
    "F#": 0.2,
    "G": 1,
    "G#": 0.2,
}
VERSE_SCHEMA = {'abba', 'abab', 'abcb', 'abb', 'aba'}
TIME_SIGNATURES = {'4/4', '3/4'}


def random_mode_of_chord(chord):
    # Maybe make a minor chord:
    minor = random.random() < .5
    if minor:
        new_chord_index = NOTES.index(chord) - 3
        chord = NOTES[new_chord_index]

    # Maybe make a 7th chord:
    seventh = random.random() < .15
    formatted_chord = f"{chord}{'m' if minor else ''}{'7' if seventh else ''}"
    return formatted_chord


def random_common_guitar_major_chord():
    return random.choices(tuple(GUITAR_WEIGHTS.keys()), weights=tuple(GUITAR_WEIGHTS.values()))[0]


def random_close_interval_int():
    return random.choice(
        (
            2,  # whole step up (two fifths up)
            5,  # fourth (fifth down)
            7,  # fifth
            10, # whole step down (two fifths down)
        )
    )


def random_close_interval_note(prev_note):
    prev_note_index = NOTES.index(prev_note)
    interval = random_close_interval_int()
    new_note_index = (prev_note_index + interval) % 12
    new_note = NOTES[new_note_index]
    return new_note


def make_line(num_chords_per_line, base_chord=None):
    line = [random_close_interval_note(base_chord) if base_chord else random_common_guitar_major_chord()]
    while len(line) < num_chords_per_line:
        line.append(random_close_interval_note(line[-1]))
    return [random_mode_of_chord(chord) for chord in line]


def make_verse(num_chords_per_line, base_chord=None):
    scheme = random.choice(tuple(VERSE_SCHEMA))
    unique_lines = {}
    lines = []
    for i, key in enumerate(scheme):
        if key not in unique_lines:
            unique_lines[key] = make_line(num_chords_per_line, base_chord=base_chord)
        lines.append(unique_lines[key])
    return lines


def format_verse(lines, name="verse"):
    verse = [f"[{name}]"]
    for line in lines:
        verse.append(" - ".join((chord for chord in line)))
    return "\n".join(verse)


@dataclass
class Song:
    num_introductory_verses: int  # verses not followed by a chorus
    num_chords_per_line: int
    num_verses: int
    time_signature: str
    tempo: int
    verse: List[str]
    chorus: List[str]
    capo: Optional[int] = None

    @classmethod
    def make(cls):
        num_introductory_verses = random.randrange(0, 2)
        num_chords_per_line=random.randrange(2, 5)
        base_chord=random_common_guitar_major_chord()
        return cls(
            num_introductory_verses=num_introductory_verses,
            num_chords_per_line=num_chords_per_line,
            num_verses=random.randrange(max(4, num_introductory_verses), 6),
            capo=random.choice((None, random.randrange(1, 7))),
            verse=make_verse(num_chords_per_line, base_chord=base_chord),
            chorus=make_verse(num_chords_per_line, base_chord=base_chord),
            time_signature=random.choice(tuple(TIME_SIGNATURES)),
            tempo=random.randrange(50, 120),
        )

    @property
    def header(self):
        header = [
            f"Time signature: {self.time_signature}",
            f"Tempo: {self.tempo} BPM",
            f"{self.num_introductory_verses} introductory verses (verses not followed by a chorus)",
            f"{self.num_verses} verses total",
        ]
        if self.capo:
            header.append(f"Capo {self.capo}")
        return header

    def serialize(self):
        return self.__dict__

    def json(self):
        return json.dumps(self.serialize())


def main(verbosity=0):
    print()
    song = Song.make()
    display = ['\n'.join(song.header)]
    if verbosity == 0:
        display.append(format_verse(song.verse))
        display.append(format_verse(song.chorus))
    else:
        for _ in range(song.num_introductory_verses):
            display.append(format_verse(song.verse))
        for _ in range(song.num_introductory_verses, song.num_verses):
            display.append(format_verse(song.verse))
            display.append(format_verse(song.chorus))
    print("\n\n".join(display))


def quick_parse_args():
    """It's faster to write this than to look up the correct incantations of argparse"""
    usage = (
        "-h / --help: print usage\n"
        "-v: verbose\n"
        "-vv: very verbose\n"
    )
    parsed_args = {'verbosity': 0}  # defaults
    unrecognized_args = set()
    for arg in sys.argv[1:]:
        if arg in ("-h", "--help"):
            print(usage)
            sys.exit()
        elif set(arg) == {"-", "v"}:
            verbosity_options = (logging.WARNING, logging.INFO, logging.DEBUG)
            verbosity = min(arg.count("v"), len(verbosity_options) - 1)
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
