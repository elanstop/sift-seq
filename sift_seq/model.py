import numpy as np
import pickle
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Conv1D, CuDNNLSTM
from tensorflow.keras.callbacks import ModelCheckpoint
from sklearn.model_selection import train_test_split


# tf.compat.v1.disable_eager_execution()


class FragmentClassifier(object):

    def __init__(self, input_viral_dna, input_human_dna, input_bacterial_dna, read_length, num_data, test_fraction,
                 epochs, batch_size):
        self.input_viral_dna = input_viral_dna
        self.input_human_dna = input_human_dna
        self.input_bacterial_dna = input_bacterial_dna
        self.read_length = read_length
        self.num_data = num_data
        self.test_fraction = test_fraction
        self.epochs = epochs
        self.batch_size = batch_size
        self.x_train, self.x_test, self.y_train, self.y_test = self.load_and_split()
        self.classifier = self.classifier()
        self.train = self.train()

    def load_and_split(self):
        virus_file = open(self.input_viral_dna, 'rb')
        viral_reads = pickle.load(virus_file)
        print('total number of viral reads in input:', len(viral_reads))
        virus_file.close()

        human_file = open(self.input_human_dna, 'rb')
        human_reads = pickle.load(human_file)
        print('total number of human reads in input:', len(human_reads))
        human_file.close()

        bacterial_file = open(self.input_bacterial_dna, 'rb')
        bacterial_reads = pickle.load(bacterial_file)
        print('total number of bacterial reads in input:', len(bacterial_reads))
        human_file.close()

        x = np.array(viral_reads[:self.num_data] + human_reads[:self.num_data] + bacterial_reads[:self.num_data])
        y = np.array([[0, 0, 1]] * self.num_data + [[0, 1, 0]] * self.num_data + [[1, 0, 0]] * self.num_data)

        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=self.test_fraction)

        return x_train, x_test, y_train, y_test

    def classifier(self):
        model = Sequential()
        # model.add(Dropout(0.5))
        model.add(Dropout(0.2, input_shape=(self.read_length, 4)))
        # model.add(Conv1D(8, 4, input_shape=(self.read_length, 4), activation='relu'))
        model.add(Conv1D(8, 4, activation='relu'))
        # dropout layer below is new
        model.add(Dropout(0.5))
        # model.add(LSTM(97, input_shape=(97, 8)))
        if tf.test.is_gpu_available():
            print("Found GPU - Training with CuDNNLSTM")
            model.add(CuDNNLSTM(100, return_sequences=False))
        else:
            model.add(LSTM(100, return_sequences=False))
        # model.add(LSTM(100))
        model.add(Dropout(0.5))
        model.add(Dense(3, activation='softmax'))
        # model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
        model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])
        return model

    def train(self):
        model_checkpoint = ModelCheckpoint('super_model.{epoch:02d}-{val_categorical_accuracy:.2f}.hdf5')
        classifier = self.classifier
        x_train, y_train = self.x_train, self.y_train
        x_test, y_test = self.x_test, self.y_test
        classifier.fit(x_train, y_train, batch_size=self.batch_size, epochs=self.epochs,
                       validation_data=(x_test, y_test), callbacks=[model_checkpoint])


if __name__ == "__main__":
    FragmentClassifier('encoded_viral_reads.txt',
                       'encoded_human_reads.txt',
                       'encoded_bacterial_reads.txt', read_length=100,
                       num_data=395000, test_fraction=0.2,
                       epochs=20, batch_size=100)
