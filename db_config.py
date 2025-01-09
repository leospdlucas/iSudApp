import psycopg2
import os
from psycopg2 import pool
from psycopg2.pool import SimpleConnectionPool

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://dbisudapp_user:1PJYJzhzrw5luUJyDHGho82lVUEnLVib@dpg-cttcvvogph6c738i0n90-a/dbisudapp")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não foi configurado.")

# Configurações do banco de dados
DB_SETTINGS = {
    'dbname': 'DBISUDAPP',
    'user': 'ISUDAPP_USER',
    'password': '25802580',
    'host': 'localhost',
    'port': '5432'
}

# Criando um pool de conexões
connection_pool = SimpleConnectionPool(
    minconn = 1,
    maxconn = 10,
    dsn = DATABASE_URL
)

def get_db_connection():

    return connection_pool.getconn()

def close_db_connection(conn):

    connection_pool.putconn(conn)

def close_all_connections():
    """
    Fecha todas as conexões do pool.
    """
    if connection_pool:
        connection_pool.closeall()
