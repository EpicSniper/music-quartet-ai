from preprocess import load_pieces_in_midi
import music21 as m21

piece = load_pieces_in_midi("MIDI/test1")
print(piece[0])
parts = []

for part in piece[0]:
    print(part)
    if isinstance(part, m21.stream.Part):
        for measure in part:
            print(measure)
            for event in measure:
                print(event)