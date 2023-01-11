from training_sequences import generate_from_file
from preprocess import SEQUENCE_LENGTH, NAME_SUFFIX, create_dataset_files, preprocess
import os
import tensorflow.keras as keras

ROOT_DIRECTORY = os.path.realpath("../..")
TEST_DATASET_PATH = ROOT_DIRECTORY + "/datasets/tests"
MODELS_DIRECTORY = ROOT_DIRECTORY + "/models"
MIDI_TEST_DATASET_PATH = ROOT_DIRECTORY + "/MIDI/test_sample"
SINGLE_TEST_FILE_DATASET = "test_dataset_file"

model_paths = [os.path.join(MODELS_DIRECTORY, f) for f in os.listdir(MODELS_DIRECTORY) if f.endswith('.h5')]
#models = [keras.models.load_model(path) for path in model_paths]

print(ROOT_DIRECTORY)
os.makedirs(TEST_DATASET_PATH, exist_ok=True)

preprocess(MIDI_TEST_DATASET_PATH, TEST_DATASET_PATH)
create_dataset_files(TEST_DATASET_PATH, SINGLE_TEST_FILE_DATASET, SEQUENCE_LENGTH)

# inputs, targets = generate_from_file(SEQUENCE_LENGTH, )