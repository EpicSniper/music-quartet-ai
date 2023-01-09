import json

ROOT_DIRECTORY = "../.."
MAPPING_PATH = ROOT_DIRECTORY + "/mapping.json"
SYMBOL_REST = "r"
SYMBOL_END_OF_PIECE = "/"
SYMBOL_EXTENDER = "_"
PITCH_MINIMUM = 20           # default 0
PITCH_MAXIMUM = 110         # default 127

def create_mapping_from_dataset(mapping_path=MAPPING_PATH):
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

def create_mapping_all(mapping_path=MAPPING_PATH):
    mappings = {}

    # rozmezi vysky tonu v midi
    for i in range(0, PITCH_MAXIMUM - PITCH_MINIMUM + 1):
        mappings[i + PITCH_MINIMUM] = i
    
    # pridani symbolu pro pomlku, konce skladby a prodlouzeni noty/pomlky
    mappings[SYMBOL_REST] = PITCH_MAXIMUM - PITCH_MINIMUM + 1
    mappings[SYMBOL_END_OF_PIECE] = PITCH_MAXIMUM - PITCH_MINIMUM + 2
    mappings[SYMBOL_EXTENDER] = PITCH_MAXIMUM - PITCH_MINIMUM + 3

    # ulozeni json souboru za ucelem mapovani
    with open(mapping_path, "w") as fp:
        json.dump(mappings, fp, indent=4)

if __name__ == "__main__":
    create_mapping_all()