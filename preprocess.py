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
    """Boolean routine that returns True if piece has all acceptable duration, False otherwise.

    :param song (m21 stream):
    :param acceptable_durations (list): List of acceptable duration in quarter length
    :return (bool):
    """
    # pridat nasobek 0.25
    for note in piece.flat.notesAndRests:
        if note.duration.quarterLength not in acceptable_durations:
            return False
    return True

def preprocess (dataseyt_path):

    # nahrat vsechny skladby
    print("Loading pieces...")
    songs = load_pieces_in_midi(dataseyt_path)
    print(f"Loaded {len(pieces)} pieces.")

    # vyfiltrovat skladby, kde jsou trioly, neni 4/4 atd.

    # transponovat skladbu do C dur nebo A mol (bez predznamenani)

    # zakodovat skladby do formatu, kteremu bude neuronka rozumnet

    # ulozit data skladeb do txt souboru

print("yey")

if __name__ == "__main__":

    pieces = load_pieces_in_midi(MIDI_DATASET_PATH)
    print(f"Loaded {len(pieces)} pieces.")
    piece = pieces[0]

    print(f"Has acceptable duration? {has_acceptable_durations(piece, ACCEPTABLE_DURATIONS)}")
    piece.show()