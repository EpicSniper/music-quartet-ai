import os
import music21 as m21
import json
import tensorflow.keras as keras
import numpy as np

MIDI_DATASET_PATH = "MIDI/training_sample"
SAVE_DIR = "dataset"
SINGLE_FILE_DATASET = "file_dataset"
MAPPING_PATH = "mapping.json"
SEQUENCE_LENGTH = 128
DATASET_PART_PATH = "file_dataset_parts"

# delka je v hodnotach ctvrtinove noty (ctvrtova nota = 1, cela nota = 4)
MIN_ACCEPTABLE_DURATION = 1/4

def load_pieces_in_midi(dataset_path):

    pieces = []
    
    # projit vsechny cesty a nahrat mid soubory
    for path, subdirs, files in os.walk(dataset_path):
        for file in files:
            if file[-3:] == "mid":
                print(file)
                piece = m21.converter.parse(os.path.join(path, file))
                pieces.append(piece)
    return pieces

def has_acceptable_durations(piece, min_acceptable_duration):
    for note in piece.flat.notesAndRests:
        if ((note.duration.quarterLength % min_acceptable_duration) > 0.001):
            print(note.duration.quarterLength)
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

def preprocess (dataset_path):

    # nahrat vsechny skladby
    print("Loading pieces...")
    pieces = load_pieces_in_midi(dataset_path)
    print(f"Loaded {len(pieces)} pieces.")

    for i, piece in enumerate(pieces):

        # vyfiltrovat skladby, kde jsou trioly, neni 4/4 atd.
        if not has_acceptable_durations(piece, MIN_ACCEPTABLE_DURATION):
            continue

        # transponovat skladbu do C dur nebo A mol (bez predznamenani)
        piece = transpose(piece)

        # zakodovat skladby do formatu, kteremu bude neuronka rozumnet
        encoded_piece = encode_piece(piece)

        # ulozit data skladeb do souboru
        save_path = os.path.join(SAVE_DIR, str(i) + "-128")
        with open(save_path, "w") as fp:
            fp.write(encoded_piece)

def encode_piece(piece, time_step=MIN_ACCEPTABLE_DURATION):
    # pitch = 60, duration = 1 -> [60, "_", "_", "_"] <- pro jednu stopu
    # ve skutecnosti je vysledny string prokladany vsemi party postupne

    encoded_piece = []
    parts = []
    encoded_parts = []
    for part in piece:
        if isinstance(part, m21.stream.Part):
            parts.append(part)

    for part in parts:
        encoded_part = []
        for event in part.flat.notesAndRests:

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
            steps = int (event.duration.quarterLength / time_step)
            for step in range(steps):
                if step == 0:
                    encoded_part.append(symbol)
                else:
                    encoded_part.append("_")
        
        encoded_parts.append(encoded_part)
    
    # zpracovani do stringu
    max_part_length = [len(encoded_parts[0]), encoded_parts[0]]
    for part in encoded_parts:
        if max_part_length[0] < len(part):
            max_part_length[0] == len(part)
            max_part_length[1] == part

    for part in encoded_parts:
        part_length = len(part)
        while (part_length) < max_part_length[0]:
            if part_length % (4 / MIN_ACCEPTABLE_DURATION) == 0:
                part_length = part_length + 1
                part.append("r")
            
            part_length = part_length + 1
            part.append("_")
            
    for i, _ in enumerate(max_part_length[1]):
        for part in encoded_parts:
            encoded_piece.append(part[i])

    encoded_piece = " ".join(map(str, encoded_piece))

    return encoded_piece

def load(file_path):
    with open(file_path, "r") as fp:
        piece = fp.read()

    return piece

def create_dataset_files(dataset_path, file_datase_path, sequence_length):

    new_piece_delimiter = "/ " * sequence_length
    pieces = ""
    piece_counter = 0
    dataset_counter = 0
    dataset_part = ""
    part0 = ""
    # nacist zakodovane skladby a pridat delimitery
    for path, _, files in os.walk(dataset_path):
        for file in files:
            file_path = os.path.join(path, file)
            piece = load(file_path)
            pieces = pieces + piece + " " + new_piece_delimiter

            dataset_part = dataset_part + piece + " " + new_piece_delimiter
            piece_counter = piece_counter + 1
            if piece_counter == 5:
                dataset_part = dataset_part[:-1]
                if (dataset_counter == 0):
                    part0 = dataset_part
                with open(DATASET_PART_PATH + "/file_dataset_part" + str(dataset_counter), "w") as fp:
                    fp.write(dataset_part)
                    dataset_part = ""
                
                dataset_counter = dataset_counter + 1
                piece_counter = 0
    
    pieces = pieces[:-1]
    dataset_part = dataset_part[:-1]

    # ulozit string, kde jsou vsechny datasety
    with open(DATASET_PART_PATH + "/file_dataset_part" + str(dataset_counter), "w") as fp:
        fp.write(dataset_part)

    with open(file_datase_path, "w") as fp:
        fp.write(pieces)

    return pieces

def create_mapping(pieces, mapping_path):
    mappings = {}

    # vytvorit slovnik
    pieces = pieces.split()
    vocabulary = list(set(pieces))

    # vytvoreni mapovani pro slovnik
    for i, symbol in enumerate(vocabulary):
        mappings[symbol] = i

    # ulozeni json souboru za ucelem mapovani
    with open(mapping_path, "w") as fp:
        json.dump(mappings, fp, indent=4)

def convert_pieces_to_int(pieces):
    int_pieces = []

    # nacist soubor s mapovanim
    with open(MAPPING_PATH, "r") as fp:
        mappings = json.load(fp)

    # prekonvertovat string skladeb na list
    pieces = pieces.split()

    # namapovat skladby na integery
    for symbol in pieces:
        int_pieces.append(mappings[symbol])
    
    return int_pieces

def generate_training_sequences(sequence_length, file_dataset):


    # nacist skladby a namapovat je na integery
    pieces = load(file_dataset)
    int_pieces = convert_pieces_to_int(pieces)

    # generace trenovaci sekvence
    # 200 symbolu, koukam dozadu na 64 symbolu, 200 - 64 = 136 pruchodu
    inputs = []
    targets = []
    num_sequences = len(int_pieces) - sequence_length
    for i in range(num_sequences):
        inputs.append(int_pieces[i:i+sequence_length])
        targets.append(int_pieces[i+sequence_length])

    # one-hot kodovani sekvence
    vocabulary_size = len(set(int_pieces)) + 1

    inputs = keras.utils.to_categorical(inputs, num_classes=vocabulary_size, dtype='float64')
    targets = np.array(targets)

    return inputs, targets

def add_mapping_to_end():
    append_part = " "
    with open(MAPPING_PATH, "r") as fp:
        mappings = json.load(fp)
    
    for word in mappings:
        append_part = append_part + " " + word
    
    for path, subdirs, files in os.walk(DATASET_PART_PATH):
        for file in files:
            with (open(path + "/" + file, "a")) as fp:
                fp.write(append_part)

def main():
    preprocess(MIDI_DATASET_PATH)
    pieces = create_dataset_files(SAVE_DIR, "file_seed", SEQUENCE_LENGTH)
    create_mapping(pieces, MAPPING_PATH)
    add_mapping_to_end()

if __name__ == "__main__":
    main()