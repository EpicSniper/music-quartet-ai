from preprocess import generate_training_sequences, SEQUENCE_LENGTH
import tensorflow.keras as keras

OUTPUT_UNITS = 19
NUM_UNITS = [256]           # [256, 256]
LOSS = "sparse_categorical_crossentropy"
LEARNING_RATE = 0.001
EPOCHS = 50                 # 40 az 100
BATCH_SIZE = 20
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


def train(output_units=OUTPUT_UNITS, num_units=NUM_UNITS, loss=LOSS, learning_rate=LEARNING_RATE):
    
    # generace treninkovych sekvenci
    inputs,targets = generate_training_sequences(SEQUENCE_LENGTH)

    # sestavit sit
    model = build_model(output_units, num_units, loss, learning_rate)

    # trenovani modelu
    model.fit(inputs, targets, epochs=EPOCHS, batch_size=BATCH_SIZE)

    # ulozit model
    model.save(SAVE_MODEL_PATH)


if __name__ == "__main__":
    train()