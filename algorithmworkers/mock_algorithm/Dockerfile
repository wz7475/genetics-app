FROM python:3.8

# ========================================
#     Steps shared for all algorithms
# ========================================
WORKDIR /code
COPY ./pangolin /code/algorithmworkers/algorithm
COPY ./common /code/algorithmworkers/common

RUN pip install --no-cache-dir --upgrade -r /code/algorithmworkers/algorithm/requirements.txt

CMD ["python3", "-m", "algorithmworkers.algorithm.main"]