import numpy as np
import pickle
import tensorflow as tf
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense, LSTM, Dropout, Conv1D, Flatten, TimeDistributed
from tensorflow.python.keras.optimizers import Adam
from sklearn.model_selection import train_test_split

#file from which to pull viral reads
input_viral_DNA = 'viral_length_100_reads.txt'

#file from which to pull human reads
input_human_DNA = 'more_human_length_100_reads.txt'

#name of trained model
saved_model = 'saved_model.h5'

#file in which the training subset is saved after splitting with train_test_split
saved_training_data = 'saved_training_data.txt'

#file in which the testing subset is saved after splitting with train_test_split
saved_test_data = 'saved_test_data.txt'

#length of supplied reads
read_length = 100

#how many reads to pull from each of the two DNA sources
num_data = 1000

#what fraction of the data to save for testing
test_fraction = 0.2

epochs = 10

batch_size = 100




class fragment_classifier(object):
	
	def __init__(self):
		self.x_train, self.x_test, self.y_train, self.y_test = self.load_and_split()
		self.classifier = self.classifier()
		self.train = self.train()

		

	def load_and_split(self):

		virus_file = open(input_viral_DNA,'rb')
		viral_reads = pickle.load(virus_file)
		virus_file.close()

		human_file = open(input_human_DNA,'rb')
		human_reads = pickle.load(human_file)
		human_file.close()

		X = np.array(viral_reads[:num_data] + human_reads[:num_data])
		Y = np.array([0]*num_data+[1]*num_data)

		x_train, x_test, y_train, y_test = train_test_split(X,Y,test_size=test_fraction)

		test_file = open(saved_test_data,'wb')
		pickle.dump([x_test,y_test],test_file)
		test_file.close()

		training_file = open(saved_training_data,'wb')
		pickle.dump([x_train,y_train],training_file)
		training_file.close()

		return x_train, x_test, y_train, y_test

	def classifier(self):
		model = Sequential()
		model.add(Dropout(0.5))
		model.add(Conv1D(8,4,input_shape=(read_length,4),activation='relu'))
		model.add(Dropout(0.5))
		model.add(LSTM(97,input_shape=(97,8)))
		model.add(Dense(1,activation='sigmoid'))
		model.compile(optimizer=Adam(),loss='binary_crossentropy',metrics=['accuracy'])
		return model

	def train(self):
		classifier = self.classifier
		x_train, y_train = self.x_train, self.y_train
		x_test, y_test = self.x_test, self.y_test
		classifier.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_data=(x_test,y_test))
		classifier.save(saved_model)



fragment_classifier()





