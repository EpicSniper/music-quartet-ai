from preprocess import SEQUENCE_LENGTH, DATASET_PART_PATH, MIN_ACCEPTABLE_DURATION, NAME_SUFFIX
from mapping import MAPPING_PATH
from training_sequences import generate_from_file, generate_using_checkpoint
import tensorflow.keras as keras
import json
import os
import datetime
import log

ROOT_DIRECTORY = "../.."
OUTPUT_UNITS = len(json.load(open(MAPPING_PATH, "r")))
NUM_UNITS = [256]           # [256] [256, 256, 256, 256]
LOSS = "sparse_categorical_crossentropy"
LEARNING_RATE = 0.001
WEIGHT_DECAY = 0.001
EPOCHS = 5                 # 40 - 100
BATCH_SIZE = 64
MODEL_NAME = "model-" + str(int(1/MIN_ACCEPTABLE_DURATION)) + "-" + str(SEQUENCE_LENGTH) + ".h5"
SAVE_MODEL_PATH = ROOT_DIRECTORY + "/" + MODEL_NAME
SAVE_BACKUP_MODEL_PATH = ROOT_DIRECTORY + "/models"


def build_model(output_units, num_units, loss, learning_rate):


    # create architecture of model
    input = keras.layers.Input(shape=(None, output_units))
    x = keras.layers.LSTM(num_units[0], kernel_regularizer=keras.regularizers.l2(WEIGHT_DECAY))(input)
    x = keras.layers.Dropout(0.2)(x)

    output = keras.layers.Dense(output_units, activation="softmax", kernel_regularizer=keras.regularizers.l2(WEIGHT_DECAY))(x)

    model = keras.Model(input, output)

    # model compile
    model.compile(loss=loss, optimizer=keras.optimizers.Adam(learning_rate=learning_rate), metrics=["accuracy"])
    model.summary()

    return model


def train(dataset_file="", output_units=OUTPUT_UNITS, num_units=NUM_UNITS, loss=LOSS, learning_rate=LEARNING_RATE):
    print(SAVE_MODEL_PATH)
    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    
    # generace treninkovych sekvenci
    inputs, targets = generate_inputs_and_targets(SEQUENCE_LENGTH, dataset_file)

    model = load_model(output_units, num_units, loss, learning_rate)
            
    # train model
    model.fit(inputs, targets, epochs=EPOCHS, batch_size=BATCH_SIZE)

    # save model
    save_model(model, dataset_file)

def load_model(output_units, num_units, loss, learning_rate):
    if os.path.exists(SAVE_MODEL_PATH):
        return keras.models.load_model(SAVE_MODEL_PATH)
    else:
        return build_model(output_units, num_units, loss, learning_rate)

def save_model(model, dataset_file):
    model.save(SAVE_MODEL_PATH)
    model.save(SAVE_BACKUP_MODEL_PATH + "/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + MODEL_NAME)
    if dataset_file == "":
        update_checkpoint(read_checkpoint() + 1)

def train_from_file(path, file):
    train(os.path.join(path, file))
    # smaze nauceny dataset
    os.remove(path + "/" + file)

def generate_inputs_and_targets(sequence_length, dataset_file):
    if dataset_file != "":
        return generate_from_file(sequence_length, dataset_file)
    else:
        return generate_using_checkpoint(sequence_length, read_checkpoint())

def train_using_checkpoints():
    print("Checkpoint number: " + str(read_checkpoint()))
    log.logMessage("Checkpoint number: " + str(read_checkpoint()))
    train()

def train_using_parts():
    for path, subdirs, files in os.walk(DATASET_PART_PATH):
        for file in files:
            if file.endswith(NAME_SUFFIX):
                print(file)
                train_from_file(path, file)
                
    print("No dataset part found!")
    log.logMessage("No dataset part found!")

def read_checkpoint():
    try:
        with open(ROOT_DIRECTORY + "/checkpoint" + NAME_SUFFIX, "r") as f:
            return int(f.read())
    except IOError:
        update_checkpoint(0)
        return 0

def update_checkpoint(checkpoint_number):
    with open(ROOT_DIRECTORY + "/checkpoint" + NAME_SUFFIX, "w") as f:
        f.write(str(checkpoint_number))
        log.logMessage("Checkpoint updated to number " + str(checkpoint_number))

def main():
    train_using_checkpoints()
    # train_using_parts()
    # train_from_file(path_to_file)

if __name__ == "__main__":
    main()
            