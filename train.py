from preprocess import generate_training_sequences, SEQUENCE_LENGTH, DATASET_PART_PATH
import tensorflow.keras as keras
import json
import os

OUTPUT_UNITS = len(json.load(open("mapping.json", "r")))
NUM_UNITS = [256]           # [256, 256]
LOSS = "sparse_categorical_crossentropy"
LEARNING_RATE = 0.001
EPOCHS = 50                 # 40 az 100
BATCH_SIZE = SEQUENCE_LENGTH
SAVE_MODEL_PATH = "model.h5"


def build_model(output_units, num_units, loss, learning_rate):


    # vytvorit architekturu modelu
    input = keras.layers.Input(shape=(None, output_units))
    x = keras.layers.LSTM(num_units[0])(input)
    x = keras.layers.Dropout(0.2)(x)

    output = keras.layers.Dense(output_units, activation="softmax")(x)

    model = keras.Model(input, output)

    # kompilovani modelu
    model.compile(loss=loss, optimizer=keras.optimizers.Adam(learning_rate=learning_rate), metrics=["accuracy"])
    model.summary()

    return model


def train(dataset_file, output_units=OUTPUT_UNITS, num_units=NUM_UNITS, loss=LOSS, learning_rate=LEARNING_RATE):
    
    # generace treninkovych sekvenci
    inputs, targets = generate_training_sequences(SEQUENCE_LENGTH, dataset_file)

    # sestavit sit
    model = build_model(output_units, num_units, loss, learning_rate)
    #model = keras.models.load_model("model.h5")

    # trenovani modelu
    model.fit(inputs, targets, epochs=EPOCHS, batch_size=BATCH_SIZE)

    # ulozit model
    model.save(SAVE_MODEL_PATH)


if __name__ == "__main__":
    for path, subdirs, files in os.walk(DATASET_PART_PATH):
        for file in files:
            train(os.path.join(path, file))