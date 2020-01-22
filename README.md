# Insight_Project
Classification of short genetic sequences

Requirements:

-Biopython 1.76. May be installed from the command line with

$conda install -c conda-forge biopython 

-TensorFlow 1.13.2. May be installed from the command line with

$conda install -c conda-forge tensorflow

Usage:

Human genetic data stored in minimal_human_data.fasta, and viral genetic data stored in minimal_viral_data.fasta. These files are preprocessed with human_genome_to_reads.py and viral_genome_to_reads.py, respectively. The output processed data files can then be used to train the model with cnn_lstm_fragment_classifier.py. Finally, the trained model can be further investigated with test_pre_trained_fragment_classifier.py.


