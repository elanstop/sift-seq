import pickle
import numpy as np
from random import shuffle
import pandas as pd
from Bio import SeqIO


class ProcessGenomeData:
    def __init__(self, input_filename, output_filename, read_length=100, genome_type='DNA',
                 max_reads_per_record=1.33 * 10 ** 5, record_limit=10 ** 10, shuffle_sequences=True, predict=False):
        self.read_set = self.split_reads(input_filename, read_length, max_reads_per_record,
                                         record_limit, shuffle_sequences)
        self.code_dict = self.make_nucleo_dict(genome_type)
        self.one_hot_encoding = self.encoding()
        self.output = self.output(output_filename, predict)

    @staticmethod
    def make_nucleo_dict(genome_type):
        if genome_type == 'DNA':
            nucleo_list = ['A', 'C', 'G', 'T', 'a', 'c', 'g', 't']
        if genome_type == 'RNA':
            nucleo_list = ['A', 'C', 'G', 'U', 'a', 'c', 'g', 'u']
        one_hots = np.eye(4, 4)
        code_list = [one_hots[i] for i in range(4)] * 2
        code_dict = dict(zip(nucleo_list, code_list))
        return code_dict

    @staticmethod
    def split_reads(input_filename, read_length, max_reads_per_record, record_limit, shuffle_sequences):
        reads_list = []
        record_count = 0
        for record in SeqIO.parse(input_filename, "fasta"):
            sequence = record.seq
            seq_length = len(sequence)
            read_count = 0
            while read_count < max_reads_per_record and read_count < seq_length - read_length:
                this_read = sequence[read_count:read_count + read_length]
                if 'N' in this_read or 'n' in this_read:
                    read_count += 1
                    max_reads_per_record += 1
                    continue
                read_count += 1
                reads_list.append(this_read)
            record_count += 1
            if record_count == record_limit:
                print('HIT RECORD LIMIT AT', record_limit, 'RECORDS')
                if shuffle_sequences:
                    shuffle(reads_list)
                    return reads_list
                else:
                    return reads_list
        if shuffle_sequences:
            shuffle(reads_list)
            return reads_list
        else:
            return reads_list

    def encoding(self):
        encoded_reads_list = []
        for read in self.read_set:
            encoded_read = []
            for letter in read:
                new_letter = self.code_dict[str(letter)]
                encoded_read.append(new_letter)
            encoded_reads_list.append(encoded_read)
        return encoded_reads_list

    def output(self, output_filename, predict):
        encoded_reads_list = self.one_hot_encoding
        if predict:
            sequences = self.read_set
            df = pd.DataFrame()
            df['Sequence'] = sequences
            df.to_csv(output_filename)
            intermediate_file = open('/data/encoded_reads_to_predict.txt', 'wb')
            pickle.dump(encoded_reads_list, intermediate_file)
            intermediate_file.close()
        else:
            output_file = open(output_filename, 'wb')
            pickle.dump(encoded_reads_list, output_file)
            output_file.close()



