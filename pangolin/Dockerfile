# Use a Python base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /code

# Download GRCh38 genomic data files
RUN wget https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_38/GRCh38.primary_assembly.genome.fa.gz
RUN wget https://www.dropbox.com/sh/6zo0aegoalvgd9f/AADOhGYJo8tbUhpscp3wSFj6a/gencode.v38.annotation.db

# Install older version of setuptools as required for pyvcf
RUN pip install "setuptools<58" --upgrade

# Install PyTorch (CPU version)
RUN pip install torch --index-url https://download.pytorch.org/whl/cpu

# Install necessary Python packages
RUN pip install pyvcf gffutils biopython pandas pyfastx

# Clone the Pangolin repository
RUN git clone https://github.com/tkzeng/Pangolin.git

# Install Pangolin
RUN cd Pangolin && pip install . && cd ..

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt