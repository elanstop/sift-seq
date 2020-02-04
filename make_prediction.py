from encoder import SeqEncoder
from predict import ModelOutput
import sys

SeqEncoder(sys.argv[1], sys.argv[2])
ModelOutput('encoded_reads.txt', sys.argv[2])
