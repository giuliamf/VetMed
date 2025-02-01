import psycopg2
from psycopg2 import sql

def get_db_connection():
    conn = psycopg2.connect(
        dbname="seu_banco_de_dados",
        user="seu_usuario",
        password="sua_senha",
        host="localhost",
        port="5432"
    )
    return conn