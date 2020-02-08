# SiftSeq
A neural network model that predicts whether 100-base sequences of DNA are viral, human, or bacterial in origin

# Contents

- **data**: contains small fasta files to make sure train.py and make_prediction.py run properly

- **sift_seq**: classes used in training and prediction

- **Dockerfile**: the file from which the docker image for this project is built

- **current_best.hdf5**: the best pre-trained model found to date

- **make_prediction.py**: the script for predicting sequence origins

- **make_prediction.py**: the script for training the neural network

# Installation

1. If you do not yet have it, download [Docker](https://www.docker.com/get-started).

2. Pull the docker image for SiftSeq from Docker Hub. On the command line, type

```shell
docker pull siftseq
```
3. Run a container from this image. On the command line, type

```shell
docker run -it siftseq
```

# Usage

To examine predictions, e.g., for the input file raw_human_reads.fasta contained in the data folder, run the following from within the container:

```shell
python make_prediction.py data/raw_human_reads.fasta output.csv
```

where output.csv is the chosen name of the output file that will hold the predictions. More generally, input files stored on your machine may be copied to the container using [docker cp](https://docs.docker.com/engine/reference/commandline/cp/).

To train the model using the example data, run the following from within the container:

```shell
python train.py
```

Trained models are saved after each epoch and labelled with their validation accuracy. To supply your own training data, simply use [docker cp](https://docs.docker.com/engine/reference/commandline/cp/) to transfer files to the container, and modify the paths within train.py to point to your chosen files.









