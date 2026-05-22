import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="",# change this 
        user="postgres",
        password="",   # change this
        port="5432"
    )
    return conn