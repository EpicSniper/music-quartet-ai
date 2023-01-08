from preprocess import generate_training_sequences, SEQUENCE_LENGTH, DATASET_PART_PATH, MIN_ACCEPTABLE_DURATION, NAME_SUFFIX
from mapping import MAPPING_PATH
import tensorflow as tf
import tensorflow.keras as keras
import json
import os
import datetime

OUTPUT_UNITS = len(json.load(open(MAPPING_PATH, "r")))
NUM_UNITS = [256]           # [256] [256, 256, 256, 256]
LOSS = "sparse_categorical_crossentropy"
LEARNING_RATE = 0.001
WEIGHT_DECAY = 0.001
EPOCHS = 5                 # 40 - 100
BATCH_SIZE = 64
SAVE_MODEL_PATH = "model-" + str(int(1/MIN_ACCEPTABLE_DURATION)) + "-" + str(SEQUENCE_LENGTH) + ".h5"


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


def train(dataset_file, output_units=OUTPUT_UNITS, num_units=NUM_UNITS, loss=LOSS, learning_rate=LEARNING_RATE):
    print(SAVE_MODEL_PATH)
    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    
    # generace treninkovych sekvenci
    inputs, targets = generate_training_sequences(SEQUENCE_LENGTH, dataset_file)

    # sestavit sit
    if os.path.exists(SAVE_MODEL_PATH):
        model = keras.models.load_model(SAVE_MODEL_PATH)
    else:
        model = build_model(output_units, num_units, loss, learning_rate) 
            
    # train model
    model.fit(inputs, targets, epochs=EPOCHS, batch_size=BATCH_SIZE)

    # save model
    model.save(SAVE_MODEL_PATH)
    model.save("models/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + SAVE_MODEL_PATH)

def train_from_file(path, file):
    train(os.path.join(path, file))
    # smaze nauceny dataset
    os.remove(path + "/" + file)

def main():
    for path, subdirs, files in os.walk(DATASET_PART_PATH):
        for file in files:
            if file.endswith(NAME_SUFFIX):
                print(file)
                train_from_file(path, file)
                
    print("No dataset part found!")

if __name__ == "__main__":
    main()
            