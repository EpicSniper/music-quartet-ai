import os
import music21 as m21

MIDI_DATASET_PATH = "MIDI/test"

# durations are expressed in quarter length
ACCEPTABLE_DURATIONS = [
    0.25, # 16th note
    0.5, # 8th note
    0.75,
    1.0, # quarter note
    1.5,
    2, # half note
    3,
    4 # whole note
]

def load_pieces_in_midi(dataset_path):

    pieces = []
    
    # projit vsechny cesty a nahrat mid soubory
    for path, subdirs, files in os.walk(dataset_path):
        for file in files:
            if file[-3:] == "mid":
                piece = m21.converter.parse(os.path.join(path, file))
                pieces.append(piece)
    return pieces

def has_acceptable_durations(piece, acceptable_durations):
    # pridat nasobek 0.25
    for note in piece.flat.notesAndRests:
        if note.duration.quarterLength not in acceptable_durations:
            return False
    return True

def transpose(piece):

    # vycist predznamenani
    parts = piece.getElementsByClass(m21.stream.Part)
    measures_part0 = parts[0].getElementsByClass(m21.stream.Measure)
    key = measures_part0[0][4]

    # odhadnout predznamenani
    if not isinstance(key, m21.key.Key):
        key = piece.analyze("key")

    # vypocitat interval pro transpozici
    if key.mode == "major":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))
    elif key.mode == "minor":
        interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))

    # transponovat skladbu podel intervalu
    transposed_piece = piece.transpose(interval)

    return transposed_piece

def preprocess (dataseyt_path):

    # nahrat vsechny skladby
    print("Loading pieces...")
    songs = load_pieces_in_midi(dataseyt_path)
    print(f"Loaded {len(pieces)} pieces.")

    for piece in pieces:

        # vyfiltrovat skladby, kde jsou trioly, neni 4/4 atd.
        if not has_acceptable_durations(piece, ACCEPTABLE_DURATIONS):
            continue

        # transponovat skladbu do C dur nebo A mol (bez predznamenani)
        piece = transpose(piece)

        # zakodovat skladby do formatu, kteremu bude neuronka rozumnet

        # ulozit data skladeb do txt souboru

if __name__ == "__main__":

    pieces = load_pieces_in_midi(MIDI_DATASET_PATH)
    print(f"Loaded {len(pieces)} pieces.")
    piece = pieces[1]

    print(f"Has acceptable duration? {has_acceptable_durations(piece, ACCEPTABLE_DURATIONS)}")

    transposed_piece = transpose(piece)

    transposed_piece.show()