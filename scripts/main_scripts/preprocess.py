import os
import music21 as m21
import sys
import log

from mapping import SYMBOL_REST, SYMBOL_END_OF_PIECE, SYMBOL_EXTENDER

ROOT_DIRECTORY = "../.."
MIDI_DATASET_PATH = ROOT_DIRECTORY + "/MIDI/training_sample"
SAVE_DIR = ROOT_DIRECTORY + "/dataset"
SINGLE_FILE_DATASET = ROOT_DIRECTORY + "/single_file_datasets/dataset_file"
SEQUENCE_LENGTH = 256
SYMBOLS_IN_DATASET_PART = 4096
# delka je v hodnotach ctvrtinove noty (ctvrtova nota = 1, cela nota = 4)
MIN_ACCEPTABLE_DURATION = 1/4
NAME_SUFFIX = "-" + str(int(1/MIN_ACCEPTABLE_DURATION)) + "-" + str(SEQUENCE_LENGTH)

def load_pieces_in_midi(dataset_path):

    pieces = []
    
    # projit vsechny cesty a nahrat mid soubory
    for path, subdirs, files in os.walk(dataset_path):
        for i, file in enumerate(files):
            if file[-3:] == "mid":
                print(str(i) + " - " + file)
                log.logMessage(str(i) + " - " + file)
                piece = m21.converter.parse(os.path.join(path, file))
                pieces.append(piece)
    return pieces

def has_acceptable_durations(piece, min_acceptable_duration, i):
    for note in piece.flat.notesAndRests:
        if (((note.duration.quarterLength + 0.0000000001) % min_acceptable_duration) > 0.000001):
            print("Note length in piece number " + str(i) + " not compatible: " + str(note.duration.quarterLength))
            log.logMessage("Note length in piece number " + str(i) + " not compatible: " + str(note.duration.quarterLength))
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
        if not has_acceptable_durations(piece, MIN_ACCEPTABLE_DURATION, i):
            continue

        # transponovat skladbu do C dur nebo A mol (bez predznamenani)
        piece = transpose(piece)

        # zakodovat skladby do formatu, kteremu bude neuronka rozumnet
        encoded_piece = encode_piece(piece)

        # ulozit data skladeb do souboru
        save_path = os.path.join(SAVE_DIR, str(i) + NAME_SUFFIX)
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
                symbol = SYMBOL_REST
            
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
                    encoded_part.append(SYMBOL_EXTENDER)
        
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
                part.append(SYMBOL_REST)
            
            part_length = part_length + 1
            part.append(SYMBOL_EXTENDER)
            
    for i, _ in enumerate(max_part_length[1]):
        for part in encoded_parts:
            encoded_piece.append(part[i])

    encoded_piece = convert_array_to_part(map(str, encoded_piece))

    return encoded_piece

def load(file_path):
    with open(file_path, "r") as fp:
        piece = fp.read()

    return piece

def create_dataset_files(dataset_path, file_datase_path, sequence_length):

    new_piece_delimiter = (SYMBOL_END_OF_PIECE + " ") * sequence_length
    pieces = ""
    # nacist zakodovane skladby a pridat delimitery
    for path, _, files in os.walk(dataset_path):
        for file in files:
            if file.endswith(NAME_SUFFIX):
                file_path = os.path.join(path, file)
                piece = load(file_path)
                pieces = pieces + piece + " " + new_piece_delimiter
    
    pieces = pieces[:-1]
    if pieces != "":
        # ulozit string, kde jsou vsechny datasety
        with open(file_datase_path + NAME_SUFFIX, "w") as fp:
            fp.write(pieces)

        return pieces
    
    print("No data available!")
    log.logMessage("No data available!")
    sys.exit()

def convert_part_to_array(part):
    return part.split(' ')

def convert_array_to_part(array):
    return " ".join(array)

def main():
    #preprocess(MIDI_DATASET_PATH)
    pieces = create_dataset_files(SAVE_DIR, SINGLE_FILE_DATASET, SEQUENCE_LENGTH)

if __name__ == "__main__":
    main()