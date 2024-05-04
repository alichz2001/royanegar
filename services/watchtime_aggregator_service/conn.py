import clickhouse_connect
import psycopg
import os

DB_PG_HOSTNAME = os.environ['DB_PG_HOSTNAME']
DB_PG_PORT = os.environ['DB_PG_PORT']
DB_PG_USER = os.environ['DB_PG_USER']
DB_PG_PASSWORD = os.environ['DB_PG_PASSWORD']
DB_PG_DATABASE_NAME = os.environ['DB_PG_DATABASE_NAME']


def get_pg_connection():
    conn_str = "postgresql://%s:%s@%s:%s/%s" % (
        DB_PG_USER,
        DB_PG_PASSWORD,
        DB_PG_HOSTNAME,
        DB_PG_PORT,
        DB_PG_DATABASE_NAME
    )
    conn = psycopg.connect(conn_str)
    return conn

def get_ch_connection():
    conn = clickhouse_connect.get_client(host='localhost')
    return conn