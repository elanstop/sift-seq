from Bio import SeqIO
import pickle

# default behavior is to output reads of length 100

# remember_species denotes whether reads are kept together with other reads from the same genome.
# default behavior is that this is false...

# reads from different genomes are mixed together


class ViralGenomeData(object):
	
	def __init__(self, input_filename, output_filename, read_length=100, genome_type='DNA', remember_species=False):
		
		self.code_list, self.code_dict = self.make_nucleo_dict(genome_type)
		self.one_hot_encoding = self.encoding(input_filename)
		self.read_set = self.split_reads(self.one_hot_encoding, read_length, remember_species)
		self.output = self.output(output_filename)

	# provide one-hot encoding for each of the nucleotides
	def make_nucleo_dict(self, genome_type):
		if genome_type == 'DNA':
			nucleo_list = ['A', 'C', 'G', 'T']
		if genome_type == 'RNA':
			nucleo_list = ['A', 'C', 'G', 'U']
		code_list = []
		for i in range(4):
			code = [0]*4
			code[i] = 1
			code_list.append(code)
		code_dict = {}
		for i in range(4):
			code_dict[nucleo_list[i]] = code_list[i]
		return code_list, code_dict

	# apply the one-hot encoding to each of the genomes in the list
	def encoding(self, input_filename):
		genome_list = []
		for record in SeqIO.parse(input_filename, "fasta"):
			this_genome = []
			for letter in record.seq:
				new_letter = self.code_dict[str(letter)]
				this_genome.append(new_letter)
			genome_list.append(this_genome)
		print('number of viral genomes in input:', len(genome_list))
		return genome_list

	# we walk along the genome, obtaining all possible reads of length equal to read_length
	def split_reads(self, genome_list, read_length, remember_species):
		reads_list = []
		if remember_species:
			for genome in genome_list:
				reads = []
				genome_length = len(genome)
				for i in range(genome_length-read_length):
					this_read = genome[i:i+read_length]
					reads.append(this_read)
				reads_list.append(reads)
		else:
			for genome in genome_list:
				genome_length = len(genome)
				for i in range(genome_length-read_length):
					this_read = genome[i:i+read_length]
					reads_list.append(this_read)
				
		return reads_list

	def output(self, output_filename):
		reads_list = self.read_set
		output_file = open(output_filename, 'wb')
		pickle.dump(reads_list, output_file)
		output_file.close()


if __name__ == "__main__":
	ViralGenomeData("minimal_virus_data.fasta", "viral_length_100_reads.txt")
