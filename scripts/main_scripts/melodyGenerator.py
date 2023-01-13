import constansts as const
import json
import tensorflow.keras as keras
import numpy as np
import music21 as m21
from music21 import instrument as inst

class PieceGenerator:

    def __init__(self, model_path=const.ACTUAL_MODEL_PATH):

        self.model_path = model_path
        self.model = keras.models.load_model(model_path)

        with open(const.MAPPING_PATH, "r") as fp:
            self._mappings = json.load(fp)
        
        self._start_symbols = [const.SYMBOL_END_OF_PIECE] * const.SEQUENCE_LENGTH

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
            if output_symbol == const.SYMBOL_END_OF_PIECE:
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

    def save_piece(self, piece, step_duration=const.MIN_ACCEPTABLE_DURATION, format="midi", filename="mastrpic.mid"):

        # vytvorit music21 stream
        stream = m21.stream.Score()

        # dekodovat noty a pomlky
        
        parts_symbols = []
        parts_symbols.append([])
        parts_symbols.append([])
        parts_symbols.append([])
        parts_symbols.append([])
        
        num_parts = len(parts_symbols)
        part_instrument = [inst.Violin(), inst.Violin(), inst.Viola(), inst.Violoncello()]
        
        # TODO: rozdelit party, aby nasledujici cyklus jel pro kazdy part zvlast

        for i, symbol in enumerate(piece):
            parts_symbols[(i%num_parts)].append(piece[i])
        
        print(parts_symbols)
        for i, part_symbols in enumerate(parts_symbols):
            part = convert_part_to_music21(parts_symbols[i], part_instrument[i], step_duration)
            stream.insert(part)
        
        # zapsat dekodovanou skladbu do midi
        stream.write(format, filename)
        return stream

        
def convert_part_to_music21(part_symbols, instrument, step_duration):
    start_symbol = None
    step_counter = 1
    stream = m21.stream.Stream()
    stream.append(instrument)
    for i, symbol in enumerate(part_symbols):
        # symbol noty nebo pomlky
        if symbol != const.SYMBOL_EXTENDER or i + 1 == len(part_symbols):
            
            if start_symbol is not None:
                duration = step_duration * step_counter     # 0.25 * 4 = 1 -> ctvrtova nota

                # symbol je pomlka
                if start_symbol == const.SYMBOL_REST:
                    m21_event = m21.note.Rest(quarterLength=duration)

                # symbol je nota
                else:
                    m21_event = m21.note.Note(int(start_symbol), quarterLength=duration)

                stream.append(m21_event)

                # resetovat pocitadlo delky a vymenit notu/pomlku
                step_counter = 1

            start_symbol = symbol

        # symbol prodlouzeni
        else:
            step_counter += 1
    return stream

if __name__ == "__main__":
    mg = PieceGenerator()
    seed = "72 67 60 48 _ _ _ _ _ _ _ 55 _ _ _ _ 72 67 _ 52 74 _ _ _ 76 67 _ 55 77 _ _ _ 79 72 64 48 _ _ _ _ 79 72 _ 55 _ _ _ _ 72 72 _ 52 _ _ _ _ _ _ _ 55 _ _ _ _ 81 77 65 53 _ _ _ _ 84 _ _ 60 _ _ _ _ 83 77 67 57 _ _ _ _ 81 _ _ 60 _ _ _ _ 79 76 64 48 _ _ _ _ _ _ _ 55 _ _ _ _ r r r 52 _ _ _ _ _ _ 64 55 _ _ _ _ 77 72 65 50 _ _ _ _ 76 69 _ 57 _ _ _ _ 77 72 64 53 _ _ _ _ 79 69 _ 57 _ _ _ _ 79 72 60 48 _ _ _ _ 76 67 _ 55 74 _ _ _ 72 72 _ 52 _ _ _ _ 76 67 _ 55 _ _ _ _ 74 67 55 50 _ _ _ _ r r r r _ _ _ _ 77 71 59 47 _ _ _ _ r r r r _ _ _ _ 76 72 60 48 _ _ _ _ 74 67 60 48 _ _ _ _ 72 64 60 48 _ _ _ _ 71 60 60 43 _ _ _ _"
    piece = mg.generate_piece(seed, 512, const.SEQUENCE_LENGTH, 1)
    print(piece)
    print(len(piece))
    stream = mg.save_piece(piece)
    stream.show()
