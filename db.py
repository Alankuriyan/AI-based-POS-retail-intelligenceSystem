import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="minix_db",
        user="postgres",
        password="alan123",   # change this
        port="5432"
    )
    return conn