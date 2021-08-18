import songemitter


def test_note_distance():
    assert songemitter.note_distance('a', 'a#') == 1
    assert songemitter.note_distance('c', 'g') == 7


def test_guitar_weights():
    chord = songemitter.random_major_chord_guitar_weighted()
    assert isinstance(chord, str)
