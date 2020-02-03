import numpy as np
import pickle
import tensorflow as tf
import pandas as pd
import sys


# classify reads using the current best pre-trained model, current_best.hdf5


class ModelOutput(object):
    def __init__(self, input_file, output_file):
        self.reverse_nucleo_dict = self.make_reverse_nucleo_dict()
        self.input_sequences = self.load_reads(input_file)
        self.prediction = self.make_prediction()
        self.encoded_input_sequences = self.encode_sequences()
        self.output_prediction = self.output_prediction(output_file)

    def make_prediction(self):
        reads = self.input_sequences

        x = np.array(reads)

        model = tf.keras.models.load_model('current_best.hdf5')
        model.compile(optimizer='Adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        prediction = model.predict(x)
        return prediction

    @staticmethod
    def make_reverse_nucleo_dict():
        nucleo_list = ['A', 'C', 'G', 'T']
        code_list = []
        for i in range(4):
            code = [0] * 4
            code[i] = 1
            code_list.append(code)
        reverse_code_dict = {}
        for i in range(4):
            reverse_code_dict[str(code_list[i])] = nucleo_list[i]
        return reverse_code_dict

    @staticmethod
    def load_reads(input_file):
        file = open(input_file, 'rb')
        reads = pickle.load(file)
        print('number of input reads:', len(reads))
        file.close()
        return reads

    def encode_sequences(self):
        sequences = self.input_sequences
        reverse_code_dict = self.reverse_nucleo_dict
        sequence_list = []
        for seq in sequences:
            this_sequence = ''
            for symbol in seq:
                nucleotide = reverse_code_dict[str(symbol)]
                this_sequence += nucleotide
            sequence_list.append(this_sequence)
        return sequence_list

    def output_prediction(self, output_file):
        prediction = self.prediction
        encoded_list = self.encoded_input_sequences

        df = pd.DataFrame()
        df['Sequence'] = encoded_list
        df['Viral prob'] = [entry[0] for entry in prediction]
        df['Human prob'] = [entry[1] for entry in prediction]
        df['Bacterial prob'] = [entry[2] for entry in prediction]
        df.to_csv(output_file)


if __name__ == "__main__":
    ModelOutput(sys.argv[1], sys.argv[2])
