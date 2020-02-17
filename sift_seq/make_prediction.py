import sys
import warnings

warnings.filterwarnings('ignore', category=DeprecationWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from model_output import ModelOutput
from preprocess import ProcessGenomeData

ProcessGenomeData('/data/' + sys.argv[1], '/' + sys.argv[2], predict=True)
ModelOutput('/data/encoded_reads_to_predict.txt', '/' + sys.argv[2])
