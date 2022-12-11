import os
import music21 as m21

MIDI_DATASET_PATH = "MIDI/test"

def load_pieces_in_midi(dataset_path):

    songs = []
    
    # projit vsechny cesty a nahrat mid soubory
    for path, subdirs, files in os.walk(dataset_path):
        for file in files:
            if file[-3] == "mid":
                song = m21.converter.parse(os.path.join(path, file))
                songs.append(song)



def preprocess (dataseyt_path):
    pass

    # nahrat vsechny skladby

    # vyfiltrovat skladby, kde jsou trioly, neni 4/4 atd.

    # transponovat skladbu do C dur nebo A mol (bez predznamenani)

    # zakodovat skladby do formatu, kteremu bude neuronka rozumnet

    # ulozit data skladeb do txt souboru
print("yey")