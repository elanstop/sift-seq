from sift_seq.viral_genomes_to_reads import ViralGenomeData
from sift_seq.human_genome_to_reads import HumanGenomeData
from sift_seq.bacterial_genomes_to_reads import BacterialGenomeData
from sift_seq.model import FragmentClassifier

ViralGenomeData("data/raw_viral_reads.fasta", 'data/encoded_viral_reads.txt')
HumanGenomeData('data/raw_human_reads.fasta', 'data/encoded_human_reads.txt')
BacterialGenomeData("data/raw_bacterial_reads.fasta", "data/encoded_bacterial_reads.txt")

# num_data refers to how many points should be pulled from each of the three files
FragmentClassifier('data/encoded_viral_reads.txt', 'data/encoded_human_reads.txt', 'data/encoded_bacterial_reads.txt',
                   read_length=100, num_data=10, test_fraction=0.2, epochs=10, batch_size=100)
