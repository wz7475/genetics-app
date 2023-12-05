from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.execute("CREATE KEYSPACE IF NOT EXISTS example WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};")
session.execute("USE example;")
session.execute("CREATE TABLE IF NOT EXISTS hello_world (id UUID PRIMARY KEY, message text);")

# To insert data
session.execute("INSERT INTO hello_world (id, message) VALUES (uuid(), 'Hello World');")

# To retrieve data
rows = session.execute("SELECT * FROM hello_world;")
for row in rows:
    print(row.id, row.message)