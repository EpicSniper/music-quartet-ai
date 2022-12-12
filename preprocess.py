import os
import music21 as m21

MIDI_DATASET_PATH = "MIDI/test"
SAVE_DIR = "dataset"
SINGLE_FILE_DATASET = "file_dataset"
SEQUENCE_LENGTH = 64

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
    if len(measures_part0[0]) >= 5:
        key = measures_part0[0][4]
    else:
        key = ""

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
    pieces = load_pieces_in_midi(dataseyt_path)
    print(f"Loaded {len(pieces)} pieces.")

    for i, piece in enumerate(pieces):

        # vyfiltrovat skladby, kde jsou trioly, neni 4/4 atd.
        if not has_acceptable_durations(piece, ACCEPTABLE_DURATIONS):
            continue

        # transponovat skladbu do C dur nebo A mol (bez predznamenani)
        piece = transpose(piece)

        # zakodovat skladby do formatu, kteremu bude neuronka rozumnet
        encoded_piece = encode_piece(piece)

        # ulozit data skladeb do souboru
        save_path = os.path.join(SAVE_DIR, str(i))
        with open(save_path, "w") as fp:
            fp.write(encoded_piece)

def encode_piece(piece, time_step=0.25):
    # pitch = 60, duration = 1 -> [60, "_", "_", "_"]
    # TODO: upravit pro vice stop, ted to dava noty za sebou bez ohledu na to, v jakem partu to je

    encoded_piece = []

    for event in piece.flat.notesAndRests:

        # zpracovani not
        if isinstance(event, m21.note.Note):
            symbol = event.pitch.midi

        # zpracovani pomlk

        if isinstance(event, m21.note.Rest):
            symbol = "r"
        
        if isinstance(event, m21.chord.Chord):
            # TODO: implementovat dvojhmaty/akordy
            # z dvojhmatu/akordu vybere ten nejnizsi ton
            symbol = event[0].pitch.midi
        
        # konvertace noty a pomlky
        # TODO: pokud budu chtit trioly (triola), tak zde zmenit time_step na 1/12 a event.duration na kratsi
        steps = int (event.duration.quarterLength / time_step)
        for step in range(steps):
            if step == 0:
                encoded_piece.append(symbol)
            else:
                encoded_piece.append("_")
    
    # zpracovani do stringu
    encoded_piece = " ".join(map(str, encoded_piece))

    return encoded_piece

def load(file_path):
    with open(file_path, "r") as fp:
        piece = fp.read()

    return piece

def create_single_file_dataset(dataset_path, file_datase_path, sequence_length):

    new_piece_delimiter = "/ " * sequence_length
    pieces = ""

    # nacist zakodovane skladby a pridat delimitery
    for path, _, files in os.walk(dataset_path):
        for file in files:
            file_path = os.path.join(path, file)
            piece = load(file_path)
            pieces = pieces + piece + " " + new_piece_delimiter
    
    pieces = pieces[:-1]

    # ulozit string, kde jsou vsechny datasety
    with open(file_datase_path, "w") as fp:
        fp.write(pieces)

    return pieces


if __name__ == "__main__":
    preprocess(MIDI_DATASET_PATH)
    pieces = create_single_file_dataset(SAVE_DIR, SINGLE_FILE_DATASET, SEQUENCE_LENGTH)