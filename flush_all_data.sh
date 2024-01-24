docker exec api bash -c "rm data/*"


python3 -c "import redis; r = redis.Redis(); r.flushall()"
echo "Flushed all data"