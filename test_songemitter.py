import songemitter

def test_note_distance():
    assert songemitter.note_distance('a', 'a#') == 1
    assert songemitter.note_distance('c', 'g') == 7
