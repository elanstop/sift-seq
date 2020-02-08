
FROM continuumio/miniconda3

RUN apt-get update


RUN conda install python=3.6.7
RUN conda install -c conda-forge tensorflow=1.13.1
RUN conda install -c conda-forge biopython
RUN conda install -c anaconda scikit-learn
RUN conda install -c anaconda pandas

RUN mkdir /data

COPY data /data
COPY bacterial_genomes_to_reads.py /
COPY current_best.hdf5 /
COPY encoder.py /
COPY human_genome_to_reads.py /
COPY make_prediction.py /
COPY model.py /
COPY model_output.py /
COPY train.py /
COPY viral_genomes_to_reads.py /


