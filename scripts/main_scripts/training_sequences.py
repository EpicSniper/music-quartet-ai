import constansts as const
import log
import tensorflow.keras as keras
import numpy as np
import json
import sys
import os
from preprocess import load, convert_part_to_array

def convert_pieces_to_int(pieces):
    int_pieces = []

    # nacist soubor s mapovanim
    with open(const.MAPPING_PATH, "r") as fp:
        mappings = json.load(fp)

    # prekonvertovat string skladeb na list
    if isinstance(pieces, str):
        pieces = pieces.split()

    # namapovat skladby na integery
    for symbol in pieces:
        int_pieces.append(mappings[symbol])
    
    return int_pieces

def get_vocabulary_size():
    return len(json.load(open(const.MAPPING_PATH, "r")))

def generate_from_file(sequence_length, file_dataset):

    log.logMessage("Getting inputs and targets from file: " + file_dataset)

    # nacist skladby a namapovat ie na integery
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
    vocabulary_size = get_vocabulary_size()

    inputs = keras.utils.to_categorical(inputs, num_classes=vocabulary_size)
    targets = np.array(targets)

    return inputs, targets

def generate_using_checkpoint(sequence_length, checkpoint_number):

    try:
        with open(const.SINGLE_FILE_DATASET_DIRECTORY + "/" + const.SINGLE_FILE_DATASET + const.NAME_SUFFIX, "r") as f:
            dataset = f.read()
    except IOError:
        print("No dataset available!")
        log.logMessage("No dataset available!")
        delete_checkpoint()
        sys.exit()
    
    dataset = convert_part_to_array(dataset)

    # Set the batch size and sequence length
    batch_size = get_batch_size()
    if batch_size < checkpoint_number:
        print("Checkpoint " + str(checkpoint_number) + " is out of range!")
        log.logMessage("Checkpoint " + str(checkpoint_number) + " is out of range!")
        if const.TRAIN_ENDLESSLY:
            delete_checkpoint()
        sys.exit()
    
    percent = round((checkpoint_number / batch_size) * 100, 2)
    message = "Checkpoint number " + str(checkpoint_number) + "/" + str(batch_size) + " (" + str(percent) +  "%)" + " in dataset " + const.SINGLE_FILE_DATASET + const.NAME_SUFFIX
    log.logMessage(message)
    print(message)
    int_pieces = convert_pieces_to_int(dataset)

    # Create empty lists to store the inputs and targets
    inputs = []
    targets = []

    # Iterate over the parts and create the inputs and targets
    for j in range(0, const.SYMBOLS_IN_DATASET_PART_MULTIPLIER):
        if checkpoint_number + j > batch_size:
            break
        for i in range(checkpoint_number, len(int_pieces) - sequence_length, batch_size):
            # Create the inputs by selecting the current sequence
            inputs.append(int_pieces[i:i+sequence_length])
            # Create the targets by selecting the next value in the sequence
            targets.append(int_pieces[i+sequence_length])
            
        checkpoint_number = checkpoint_number + 1

    # Use the inputs and targets to train your LSTM model
    vocabulary_size = get_vocabulary_size()

    inputs = keras.utils.to_categorical(inputs, num_classes=vocabulary_size)
    targets = np.array(targets)

    return inputs, targets

def get_batch_size():
    try:
        with open(const.SINGLE_FILE_DATASET_DIRECTORY + "/" + const.SINGLE_FILE_DATASET + const.NAME_SUFFIX, "r") as f:
            dataset = f.read()
    except IOError:
        print("No dataset available!")
        log.logMessage("No dataset available!")
        sys.exit()
    
    dataset = convert_part_to_array(dataset)

    # Set the batch size and sequence length
    return int(len(dataset) / const.SYMBOLS_IN_DATASET_PART)

def read_checkpoint():
    try:
        with open(const.ROOT_DIRECTORY + "/checkpoint" + const.NAME_SUFFIX, "r") as f:
            return int(f.read())
    except IOError:
        update_checkpoint(0)
        return 0

def update_checkpoint(checkpoint_number):
    with open(const.ROOT_DIRECTORY + "/checkpoint" + const.NAME_SUFFIX, "w") as f:
        f.write(str(checkpoint_number))
        log.logMessage("Checkpoint updated to number " + str(checkpoint_number))

def delete_checkpoint():
    os.remove(const.ROOT_DIRECTORY + "/checkpoint" + const.NAME_SUFFIX)
