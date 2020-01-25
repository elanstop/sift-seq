import numpy as np
import pickle
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, LSTM, Dropout, Conv1D
from tensorflow.python.keras.optimizers import Adam
from sklearn.model_selection import train_test_split


class FragmentClassifier(object):
	
	def __init__(self, input_viral_dna, input_human_dna, saved_model, saved_training_data, saved_test_data,
				 read_length, num_data, test_fraction, epochs, batch_size):
		self.input_viral_dna = input_viral_dna
		self.input_human_dna = input_human_dna
		self.saved_model = saved_model
		self.saved_training_data = saved_training_data
		self.saved_test_data = saved_test_data
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
		virus_file.close()

		human_file = open(self.input_human_dna, 'rb')
		human_reads = pickle.load(human_file)
		human_file.close()

		x = np.array(viral_reads[:self.num_data] + human_reads[:self.num_data])
		y = np.array([0]*self.num_data+[1]*self.num_data)

		x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=self.test_fraction)

		test_file = open(self.saved_test_data, 'wb')
		pickle.dump([x_test, y_test], test_file)
		test_file.close()

		training_file = open(self.saved_training_data, 'wb')
		pickle.dump([x_train, y_train], training_file)
		training_file.close()

		return x_train, x_test, y_train, y_test

	def classifier(self):
		model = Sequential()
		model.add(Dropout(0.5))
		model.add(Conv1D(8, 4, input_shape=(self.read_length, 4), activation='relu'))
		model.add(Dropout(0.5))
		model.add(LSTM(97, input_shape=(97, 8)))
		model.add(Dense(1, activation='sigmoid'))
		model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
		return model

	def train(self):
		classifier = self.classifier
		x_train, y_train = self.x_train, self.y_train
		x_test, y_test = self.x_test, self.y_test
		classifier.fit(x_train, y_train, batch_size=self.batch_size, epochs=self.epochs, validation_data=(x_test, y_test))
		classifier.save(self.saved_model)


if __name__ == "__main__":
	FragmentClassifier('viral_length_100_reads.txt', 'human_length_100_reads.txt', 'saved_model.h5',
					   'saved_training_data.txt', 'saved_test_data.txt', read_length=100, num_data=1000, test_fraction=0.2,
					   epochs=10, batch_size=100)
