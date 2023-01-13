import constansts as const
import tensorflow.keras as keras
import os
import datetime
import log
from training_sequences import generate_from_file, generate_using_checkpoint, read_checkpoint, update_checkpoint

def build_model(output_units, num_units, loss, learning_rate):
    # create architecture of model
    input = keras.layers.Input(shape=(None, output_units))
    x = keras.layers.LSTM(num_units[0], kernel_regularizer=keras.regularizers.l2(const.WEIGHT_DECAY))(input)
    x = keras.layers.Dropout(0.2)(x)

    output = keras.layers.Dense(output_units, activation="softmax", kernel_regularizer=keras.regularizers.l2(const.WEIGHT_DECAY))(x)

    model = keras.Model(input, output)

    # model compile
    model.compile(loss=loss, optimizer=keras.optimizers.Adam(learning_rate=learning_rate), metrics=["accuracy"])
    model.summary()

    return model


def train(dataset_file="", output_units=const.OUTPUT_UNITS, num_units=const.NUM_UNITS, loss=const.LOSS, learning_rate=const.LEARNING_RATE):
    print(const.ACTUAL_MODEL_PATH)
    
    # generace treninkovych sekvenci
    inputs, targets = generate_inputs_and_targets(const.SEQUENCE_LENGTH, dataset_file)

    model = load_model(output_units, num_units, loss, learning_rate)
            
    # train model
    model.fit(inputs, targets, epochs=const.EPOCHS, batch_size=const.BATCH_SIZE)

    # save model
    save_model(model, dataset_file)

def load_model(output_units, num_units, loss, learning_rate):
    if os.path.exists(const.ACTUAL_MODEL_PATH):
        return keras.models.load_model(const.ACTUAL_MODEL_PATH)
    else:
        return build_model(output_units, num_units, loss, learning_rate)

def save_model(model, dataset_file):
    model.save(const.ACTUAL_MODEL_PATH)
    os.makedirs(const.BACKUP_MODELS_DIRECTORY,exist_ok=True)
    model.save(const.BACKUP_MODELS_DIRECTORY + "/" + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + const.MODEL_NAME)
    if dataset_file == "":
        update_checkpoint(read_checkpoint() + const.SYMBOLS_IN_DATASET_PART_MULTIPLIER)

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

def main():
    train_using_checkpoints()
    # train_from_file(path_to_file)

if __name__ == "__main__":
    main()
            