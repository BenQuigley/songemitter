# Songemitter

This is a Python script for constructing simple chord progressions. It has no requirements besides
Python, so you can run it with:

    $ git clone https://github.com/BenQuigley/songemitter
    $ cd songemitter
    $ python3 songemitter

Example output:

    Time signature: 4/4
    Tempo: 81 BPM
    1 introductory verses (verses not followed by a chorus)
    4 verses total
    Capo 1

    [verse]
    D - C - F
    D# - A#m - D#m
    D# - A#m - D#m

    [chorus]
    Em - A - G
    F#m - G#m - C#m
    Em - A - G

There is also a `verbose` mode where it will print that many verses and choruses, in case you are
using it as a songwriting tool and want to use the output to start writing lyrics onto:

    $ python3 songemitter -v
