import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from sift_seq.encoder import SeqEncoder
from sift_seq.model_output import ModelOutput
import sys


SeqEncoder(sys.argv[1], sys.argv[2])
ModelOutput('data/encoded_reads_to_predict.txt', sys.argv[2])
