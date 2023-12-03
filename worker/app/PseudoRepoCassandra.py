from cassandra.cluster import Cluster


def get_cassandra_session():
    cluster = Cluster(['cassandra'])
    session = cluster.connect()
    session.execute(
        "CREATE KEYSPACE IF NOT EXISTS example WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};")
    session.execute("USE example;")
    return session
