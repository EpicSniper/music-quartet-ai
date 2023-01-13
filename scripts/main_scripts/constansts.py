import os
import json

# DATASET STRUCUTRE
SEQUENCE_LENGTH = 128           # musi byt mensi nez SYMBOLS_IN_DATASET_PART * SYMBOLS_IN_DATASET_PART_MULTIPLIER
MIN_ACCEPTABLE_DURATION = 1/4   # delka je v hodnotach ctvrtinove noty (ctvrtova nota = 1, cela nota = 4)
# SYMBOLS_IN_DATASET_PART * SYMBOLS_IN_DATASET_PART_MULTIPLIER > SEQUENCE_LENGTH (model structure)
SYMBOLS_IN_DATASET_PART = 1024
SYMBOLS_IN_DATASET_PART_MULTIPLIER = 100


# PROJECT STRUCTURE
ROOT_DIRECTORY = os.path.realpath("../..")

NAME_DIR_SUFFIX = str(int(1/MIN_ACCEPTABLE_DURATION)) + "-" + str(SEQUENCE_LENGTH)
NAME_SUFFIX = "-" + NAME_DIR_SUFFIX

SINGLE_FILE_DATASET =      "train_dataset_file"
SINGLE_TEST_FILE_DATASET = "test_dataset_file"

SINGLE_FILE_DATASET_DIRECTORY = ROOT_DIRECTORY + "/datasets/single_file_datasets"
TEST_DATASET_PATH =             ROOT_DIRECTORY + "/datasets/tests"
SAVE_DIR =                      ROOT_DIRECTORY + "/datasets/train"

MIDI_TEST_DATASET_PATH = ROOT_DIRECTORY + "/MIDI/test_sample"
MIDI_DATASET_PATH =      ROOT_DIRECTORY + "/MIDI/training_sample"


# MAPPINGS
SYMBOL_REST = "r"
SYMBOL_END_OF_PIECE = "/"
SYMBOL_EXTENDER = "_"
MAPPING_PATH = ROOT_DIRECTORY + "/mapping.json"


# MODEL STRUCTURE
MODEL_NAME = "model-" + str(int(1/MIN_ACCEPTABLE_DURATION)) + "-" + str(SEQUENCE_LENGTH) + ".h5"
ACTUAL_MODEL_PATH = ROOT_DIRECTORY + "/" + MODEL_NAME
BACKUP_MODELS_DIRECTORY = ROOT_DIRECTORY + "/models"

OUTPUT_UNITS = len(json.load(open(MAPPING_PATH, "r")))
NUM_UNITS = [256]           # [256] [256, 256, 256, 256]
LOSS = "sparse_categorical_crossentropy"
LEARNING_RATE = 0.001
WEIGHT_DECAY = 0.001
EPOCHS = 5                 # 40 - 100
TRAIN_ENDLESSLY = True
BATCH_SIZE = 64