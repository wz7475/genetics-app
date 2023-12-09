from uuid import uuid4
import redis
from logger import get_logger

def insert_random_record(r):
    value = "-15:0.8100000023841858|-2:-0.8500000238418579|Warnings:"
    key = f"{uuid4()}"
    r.hset(
        key,
        mapping={
            "alg1": value,
            "alg2": value,
        },
    )

def insert_n_random_records(r, n):
    for _ in range(n):
        insert_random_record(r)

if __name__ == "__main__":
    logger = get_logger()
    logger.info("Hello World!")
    r = redis.Redis(host="redisalg", port=6379)
    insert_n_random_records(r, 1_000_000)
    logger.info(f"Inserted 1,000,000 records into Redis.")