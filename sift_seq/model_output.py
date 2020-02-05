import numpy as np
import pickle
import tensorflow as tf
import pandas as pd
import sys


# classify reads using the current best pre-trained model, current_best.hdf5


class ModelOutput(object):
    def __init__(self, input_file, output_file):
        self.input_sequences = self.load_reads(input_file)
        self.prediction = self.make_prediction()
        self.output_prediction(output_file)
        self.get_fractions()

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
    def load_reads(input_file):
        file = open(input_file, 'rb')
        reads = pickle.load(file)
        file.close()
        return reads

    def output_prediction(self, output_file):
        prediction = self.prediction
        df = pd.read_csv(output_file)
        df['Viral prob'] = [entry[0] for entry in prediction]
        df['Human prob'] = [entry[1] for entry in prediction]
        df['Bacterial prob'] = [entry[2] for entry in prediction]
        df.to_csv(output_file)

    def get_fractions(self):
        viral_count = 0
        bacterial_count = 0
        human_count = 0
        prediction = self.prediction
        num_sequences = len(prediction)
        for i in range(num_sequences):
            this_prediction = list(prediction[i])
            identity = this_prediction.index(max(this_prediction))
            if identity == 0:
                viral_count += 1
            if identity == 1:
                human_count += 1
            if identity == 2:
                bacterial_count += 1
        print('Predicted fraction of viral sequences:', viral_count / num_sequences)
        print('Predicted fraction of human sequences:', human_count / num_sequences)
        print('Predicted fraction of bacterial sequences:', bacterial_count / num_sequences)


if __name__ == "__main__":
    ModelOutput(sys.argv[1], sys.argv[2])
