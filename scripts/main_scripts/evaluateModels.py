import constansts as const
from training_sequences import generate_from_file
from preprocess import create_dataset_files, preprocess
import os
import tensorflow.keras as keras

model_paths = [os.path.join(const.BACKUP_MODELS_DIRECTORY, f) for f in os.listdir(const.BACKUP_MODELS_DIRECTORY) if f.endswith('.h5')]
models = [keras.models.load_model(path) for path in model_paths]

print(const.ROOT_DIRECTORY)
os.makedirs(const.TEST_DATASET_DIRECTORY, exist_ok=True)

preprocess(const.MIDI_TEST_DATASET_DIRECTORY, const.TEST_DATASET_DIRECTORY)
create_dataset_files(const.TEST_DATASET_DIRECTORY, const.SINGLE_TEST_FILE_DATASET, const.SEQUENCE_LENGTH)

inputs, targets = generate_from_file(const.SEQUENCE_LENGTH, const.SINGLE_FILE_DATASET_DIRECTORY + "/" + const.SINGLE_TEST_FILE_DATASET + const.NAME_SUFFIX)

results = []

for model in model_paths:
    print(model)
    model = keras.models.load_model(model)
    evaluation = model.evaluate(inputs, targets, const.BATCH_SIZE)
    results.append([model, evaluation])

# TODO: better sorter
results.sort(key=lambda x: x[1], reverse=True)
for result in results:
    print(result[0], result[1])