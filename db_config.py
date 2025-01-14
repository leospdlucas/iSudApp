import psycopg2
import os
from psycopg2.pool import SimpleConnectionPool

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://adm_leo:6m3Z428RS0x7mfZHw7CIHr2Ih6P8pdFN@dpg-cu3a4i8gph6c73bpl2c0-a/db_isudapp")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não foi configurado.")

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
