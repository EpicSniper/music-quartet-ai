import json
import tensorflow.keras as keras
import numpy as np
from preprocess import SEQUENCE_LENGTH, MAPPING_PATH

class PieceGenerator:

    def __init__(self, model_path="model.h5"):

        self.model_path = model_path
        self.model = keras.models.load_model(model_path)

        with open(MAPPING_PATH, "r") as fp:
            self._mappings = json.load(fp)
        
        self._start_symbols = ["/"] * SEQUENCE_LENGTH

    def generate_piece(self, seed, num_steps, max_sequence_length, temperature):

        # vytvorit seed se startovnimi symboly
        seed = seed.split()
        piece = seed
        seed = self._start_symbols + seed

        # namapovat seed na integery podle jsonu
        seed = [self._mappings[symbol] for symbol in seed]

        for _ in range(num_steps):

            # limit the seed to max_sequence_length
            seed = seed[-max_sequence_length:]

            # one-hot kodovani seedu
            onehot_seed = keras.utils.to_categorical(seed, num_classes=len(self._mappings))
            # (1, max_sequence_length, num of symbols in slovnik)
            onehot_seed = onehot_seed[np.newaxis, ...]

            # udelat predikci
            probabilities = self.model.predict(onehot_seed)[0]
            output_int = self._sample_with_temperature(probabilities, temperature)

            # aktualizace seedu
            seed.append(output_int)

            # zpetne namapovani
            output_symbol = [k for k, v in self._mappings.items() if v == output_int][0]

            # zkontrolovat, jestli nejsme na konci
            if output_symbol == "/":
                break

            piece.append(output_symbol)
        
        return piece

    def _sample_with_temperature(self, probabilities, temperature):
        # temperature -> nekonecno ------> nahodne vybira dalsi notu
        # temperature -> 0 ------> deterministicky
        # temperature = 1 ------> idealka
        predictions = np.log(probabilities) / temperature
        probabilities = np.exp(predictions) / np.sum(np.exp(predictions))

        choices = range(len(probabilities))
        index = np.random.choice(choices, p=probabilities)

        return index

if __name__ == "__main__":
    mg = PieceGenerator()
    seed = "55 _ _ _ 60 _ _ _ 55 _ _ _ 55 _"
    piece = mg.generate_piece(seed, 500, SEQUENCE_LENGTH, 0.7)
    print(piece)