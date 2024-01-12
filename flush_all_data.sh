docker exec api bash -c "rm -r data/*"
echo "Flushed files in shared volume"

python3 -c "import redis
r = redis.Redis()
r.flushdb()
print('Flushed redis')
"