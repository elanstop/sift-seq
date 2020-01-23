# Insight_Project
Classification of short genetic sequences

# Requirements:

-TensorFlow 1.13.2. May be installed from the command line with

$conda create -n envname tensorflow

-Biopython 1.76. After activating the previously created virtual environment, install from the command line with

$conda install -c conda-forge biopython

-scikit-learn 0.22.1. May be installed from the command line with

$conda install -c anaconda scikit-learn

# Usage:

Human genetic data stored in minimal_human_data.fasta, and viral genetic data stored in minimal_viral_data.fasta. These files are preprocessed with human_genome_to_reads.py and viral_genome_to_reads.py, respectively. The output processed data files can then be used to train the model with cnn_lstm_fragment_classifier.py. Finally, the trained model can be further investigated with test_pre_trained_fragment_classifier.py.


