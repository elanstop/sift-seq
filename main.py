from encoder import SeqEncoder
from predict import ModelOutput
import sys


if __name__ == "__main__":
    # SeqEncoder(sys.argv[1],'encoded_reads.txt')
    # ModelOutput('encoded_reads.txt',sys.argv[2])
    SeqEncoder(sys.argv[1],sys.argv[2])
    ModelOutput('encoded_reads.txt',sys.argv[2])

	

