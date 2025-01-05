import psycopg2
from psycopg2 import pool

# Configurações do banco de dados
DB_SETTINGS = {
    'dbname': 'DBISUDAPP',
    'user': 'ISUDAPP_USER',
    'password': '25802580',
    'host': 'localhost',
    'port': '5432'
}

# Criando um pool de conexões
connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 10, **DB_SETTINGS
)

def get_db_connection():
    """
    Obtém uma conexão do pool.
    """
    if connection_pool:
        return connection_pool.getconn()

def close_db_connection(connection):
    """
    Retorna a conexão para o pool.
    """
    if connection:
        connection_pool.putconn(connection)

def close_all_connections():
    """
    Fecha todas as conexões do pool.
    """
    if connection_pool:
        connection_pool.closeall()
