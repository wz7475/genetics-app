FROM r-base:latest

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/LBGC-CFB/SPiP.git

WORKDIR /usr/src/app/SPiP

# Download necessary files into RefFiles
#RUN mkdir -p RefFiles && \
#    wget -P RefFiles [URLs of necessary files]

# Install any needed packages specified in requirements
RUN R -e "install.packages(c('foreach', 'doParallel', 'randomForest'), dependencies=TRUE)"

RUN wget -O /usr/src/app/SPiP/RefFiles/transcriptome_hg38.RData https://sourceforge.net/projects/splicing-prediction-pipeline/files/transcriptome/transcriptome_hg38.RData/download
RUN wget -O /usr/src/app/SPiP/RefFiles/transcriptome_hg19.RData https://sourceforge.net/projects/splicing-prediction-pipeline/files/transcriptome/transcriptome_hg19.RData/download

# ========================================
#     Steps shared for all algorithms
# ========================================
RUN apt-get update && apt-get install -y python3-pika
WORKDIR /code
COPY ./spip /code/algorithmworkers/algorithm
COPY ./common /code/algorithmworkers/common

CMD ["python3", "-m", "algorithmworkers.algorithm.main"]