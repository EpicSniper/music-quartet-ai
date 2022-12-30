import os
from preprocess import DATASET_PART_PATH, NAME_SUFFIX
from train import train_from_file


if __name__ == "__main__":
    for path, subdirs, files in os.walk(DATASET_PART_PATH):
        for file in files:
            if file.endswith(NAME_SUFFIX):
                train_from_file(path, file)
                
    print("No dataset part found!")