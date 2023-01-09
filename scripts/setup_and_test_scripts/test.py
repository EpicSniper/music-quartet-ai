from math import ceil
import sys
sys.path.insert(1, '../main_scripts')
import log

DATASET = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
SYMBOLS_IN_DATASET = 5
BATCH_SIZE = ceil(len(DATASET) / SYMBOLS_IN_DATASET)

def generate_using_checkpoint(sequence_length, checkpoint_number):
    # Create normal Python lists from your arrays of integers
    dataset = DATASET

    # Set the batch size and sequence length
    batch_size = BATCH_SIZE

    # Create empty lists to store the inputs and targets
    inputs = []
    targets = []

    # Iterate over the parts and create the inputs and targets
    for j in range(checkpoint_number, len(dataset) - sequence_length, batch_size):
        # Create the inputs by selecting the current sequence
        inputs.append(dataset[j:j+sequence_length])
        # Create the targets by selecting the next value in the sequence
        targets.append(dataset[j+sequence_length])

    print(inputs)
    print(targets)

if __name__ == "__main__":
    print(BATCH_SIZE)
    log.logMessage("Helloujy")
    for i in range (0, BATCH_SIZE):
        generate_using_checkpoint(3, i)
