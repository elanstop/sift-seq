from Bio import SeqIO
import pickle
import sys
import pandas as pd


class SeqEncoder(object):

    def __init__(self, input_filename, output_filename, read_length=100, genome_type='DNA'):
        self.read_set = self.split_reads(input_filename, read_length)
        self.code_list, self.code_dict = self.make_nucleo_dict(genome_type)
        self.one_hot_encoding = self.encoding()
        self.output = self.output()
        self.save_sequences(output_filename)

    # apply the one-hot encoding to each of the reads in the list
    def encoding(self):
        encoded_reads_list = []
        for read in self.read_set:
            encoded_read = []
            for letter in read:
                new_letter = self.code_dict[str(letter)]
                encoded_read.append(new_letter)
            encoded_reads_list.append(encoded_read)
        print('number of input reads:', len(encoded_reads_list))
        return encoded_reads_list

    def output(self):
        encoded_reads_list = self.one_hot_encoding
        output_file = open('encoded_reads.txt', 'wb')
        pickle.dump(encoded_reads_list, output_file)
        output_file.close()

    # provide one-hot encoding for each of the nucleotides
    # lower case letters mapped to the same one-hot symbol
    @staticmethod
    def make_nucleo_dict(genome_type):
        if genome_type == 'DNA':
            nucleo_list = ['A', 'C', 'G', 'T', 'a', 'c', 'g', 't']
        if genome_type == 'RNA':
            nucleo_list = ['A', 'C', 'G', 'U', 'a', 'c', 'g', 'u']
        code_list = []
        for i in range(4):
            code = [0] * 4
            code[i] = 1
            code_list.append(code)
        code_dict = {}
        for i in range(4):
            code_dict[nucleo_list[i]] = code_list[i]
        for i in range(4, 8):
            code_dict[nucleo_list[i]] = code_list[i - 4]
        return code_list, code_dict

    @staticmethod
    def split_reads(input_filename, read_length):
        reads_list = []
        for record in SeqIO.parse(input_filename, "fasta"):
            contig = record.seq
            i = 0
            while i <= len(contig) - read_length:
                this_read = contig[i:i + read_length]
                if 'N' in this_read or 'n' in this_read:
                    i += 1
                    continue
                i += 1
                reads_list.append(this_read)
        return reads_list

    def save_sequences(self, output_filename):
        sequences = self.read_set
        df = pd.DataFrame()
        df['Sequence'] = sequences
        df.to_csv(output_filename)


if __name__ == "__main__":
    SeqEncoder(sys.argv[1], sys.argv[2])
