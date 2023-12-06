import psycopg2

conn = psycopg2.connect(database="algorythms",
                        host="0.0.0.0",
                        user="userone",
                        password="pass",
                        port="5432")


def createTables():
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE cars ( brand VARCHAR(255), model VARCHAR(255), year INT);")