import psycopg2



def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='royanegar_user',
                            password='1234')
    return conn
