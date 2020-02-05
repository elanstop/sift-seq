from encoder import SeqEncoder
from model_output import ModelOutput
import sys

SeqEncoder(sys.argv[1], sys.argv[2])
ModelOutput('data/encoded_reads_to_predict.txt', sys.argv[2])
