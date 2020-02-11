
FROM continuumio/miniconda3

RUN apt-get update


RUN conda install python=3.6.7
RUN conda install -c conda-forge tensorflow=1.13.1
RUN conda install -c conda-forge biopython
RUN conda install -c anaconda scikit-learn
RUN conda install -c anaconda pandas

RUN mkdir /data
RUN mkdir /saved_models
RUN mkdir /sift_seq

COPY data /data
COPY saved_models /saved_models
COPY sift_seq /sift_seq


