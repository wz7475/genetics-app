# Use a Python base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

