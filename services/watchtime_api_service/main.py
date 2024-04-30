import psycopg2
from flask import Flask, render_template

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='postgres',
                            database='royanegar',
                            user='royamegar_user',
                            password='1234')
    return conn


@app.route('/api/v1/watchtime/user')
def index():

    req_user_id = args.get("id", default=0, type=int)

    

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM books;')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)
