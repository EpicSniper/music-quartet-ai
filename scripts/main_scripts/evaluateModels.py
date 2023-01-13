import constansts as const
from training_sequences import generate_from_file
from preprocess import create_dataset_files, preprocess
import os
import tensorflow.keras as keras

#model_paths = [os.path.join(MODELS_DIRECTORY, f) for f in os.listdir(MODELS_DIRECTORY) if f.endswith('.h5')]
#models = [keras.models.load_model(path) for path in model_paths]

print(const.ROOT_DIRECTORY)
os.makedirs(const.TEST_DATASET_PATH, exist_ok=True)

preprocess(const.MIDI_TEST_DATASET_PATH, const.TEST_DATASET_PATH)
create_dataset_files(const.TEST_DATASET_PATH, const.SINGLE_TEST_FILE_DATASET, Sconst.EQUENCE_LENGTH)

# inputs, targets = generate_from_file(SEQUENCE_LENGTH, )