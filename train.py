from viral_genomes_to_reads import ViralGenomeData
from human_genome_to_reads import HumanGenomeData
from bacterial_genomes_to_reads import BacterialGenomeData
from model import FragmentClassifier

ViralGenomeData("raw_viral_reads.fasta", 'encoded_viral_reads.txt')
HumanGenomeData('raw_human_reads.fasta', 'encoded_human_reads.txt')
BacterialGenomeData("raw_bacterial_reads.fasta", "encoded_bacterial_reads.txt")

# num_data refers to how many points should be pulled from each of the three files
FragmentClassifier('encoded_viral_reads.txt', 'encoded_human_reads.txt', 'encoded_bacterial_reads.txt', read_length=100,
                   num_data=10, test_fraction=0.2, epochs=10, batch_size=100)
