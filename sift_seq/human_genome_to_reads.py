from Bio import SeqIO
import pickle

# this file is different from viral_genomes_to_reads in the following ways:

# don't want to encode and return whole genome yet, because it's too much data. currently only pulling the first
# max_reads reads from the first record (chrom1)
# reads are split before encoding, so that reads including the missing nucleotide symbol "N" or "n" can be left out
# (this might be adding runtime)

# the genome includes lowercase letters as well as upper case letters

# default behavior is to pull reads of length 100


class HumanGenomeData(object):
	
	def __init__(
				self, input_filename, output_filename, read_length=100, genome_type='DNA', max_reads=6*10**5):
		self.read_set = self.split_reads(input_filename, read_length, max_reads)
		self.code_list, self.code_dict = self.make_nucleo_dict(genome_type)
		self.one_hot_encoding = self.encoding()
		self.output = self.output(output_filename)

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
			code = [0]*4
			code[i] = 1
			code_list.append(code)
		code_dict = {}
		for i in range(4):
			code_dict[nucleo_list[i]] = code_list[i]
		for i in range(4, 8):
			code_dict[nucleo_list[i]] = code_list[i-4]
		return code_list, code_dict

	# apply the one-hot encoding to each of the reads in the list
	def encoding(self):
		encoded_reads_list = []
		for read in self.read_set:
			encoded_read = []
			for letter in read:
				new_letter = self.code_dict[str(letter)]
				encoded_read.append(new_letter)
			encoded_reads_list.append(encoded_read)
		return encoded_reads_list

	# we walk along each record, obtaining all possible reads of length equal to read_length
	@staticmethod
	def split_reads(input_filename, read_length, max_reads):
		reads_list = []
		for record in SeqIO.parse(input_filename, "fasta"):
			contig = record.seq
			i = 0
			while i < max_reads and i < len(contig)-read_length:
				this_read = contig[i:i+read_length]
				if 'N' in this_read or 'n' in this_read:
					i += 1
					max_reads += 1
					continue
				i += 1
				reads_list.append(this_read)
			# STOP AFTER THE FIRST RECORD BECAUSE WE DON'T NEED ALL THIS DATA!
			return reads_list

	def output(self, output_filename):
		encoded_reads_list = self.one_hot_encoding
		output_file = open(output_filename, 'wb')
		pickle.dump(encoded_reads_list, output_file)
		output_file.close()


if __name__ == "__main__":
	HumanGenomeData("human.fa", "human_reads.txt")
















	

