import psycopg2
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

DB_PG_HOSTNAME = os.environ['DB_PG_HOSTNAME']
DB_PG_PORT = os.environ['DB_PG_PORT']
DB_PG_USER = os.environ['DB_PG_USER']
DB_PG_PASSWORD = os.environ['DB_PG_PASSWORD']
DB_PG_DATABASE_NAME = os.environ['DB_PG_DATABASE_NAME']


def get_db_connection():
    conn = psycopg2.connect(host=DB_PG_HOSTNAME,
                            database=DB_PG_DATABASE_NAME,
                            port=DB_PG_PORT,
                            user=DB_PG_USER,
                            password=DB_PG_PASSWORD)
    return conn


@app.route('/api/v1/watchtime/user')
def user_watchtime():
    args = request.args
    req_user_id = args.get('user', default="", type=str)

    if req_user_id == "" :
        return "bad user", 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT duration FROM user_watchtimes where "user" = %s;', (req_user_id,))
    user_watchtime = cur.fetchone()
    cur.close()
    conn.close()

    if user_watchtime == None:
        return "0", 200
    
    return str(user_watchtime[0]), 200

@app.route('/api/v1/watchtime/user_slug')
def user_slug_watchtime():
    args = request.args
    req_user_id = args.get('user', default="", type=str)
    req_slug_id = args.get('slug', default="", type=str)

    if req_user_id == "" :
        return "bad user", 400
    
    if req_slug_id == "" :
        return "bad slug", 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT duration FROM user_slug_watchtimes where "user_slug" = %s;', (req_user_id + "--" + req_slug_id,))
    user_slug_watchtime = cur.fetchone()
    cur.close()
    conn.close()

    if user_slug_watchtime == None:
        return "0", 200
    
    return str(user_slug_watchtime[0]), 200

@app.route('/api/v1/watchtime/slug')
def slug_watchtime():
    args = request.args
    req_slug_id = args.get('slug', default="", type=str)

    if req_slug_id == "" :
        return "bad slug", 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT duration FROM slug_watchtimes where "slug" = %s;', (req_slug_id,))
    slug_watchtime = cur.fetchone()
    cur.close()
    conn.close()

    if slug_watchtime == None:
        return "0", 200
    
    return str(slug_watchtime[0]), 200

@app.route('/api/v1/state/user_slug')
def user_slug_state():
    args = request.args
    req_user_id = args.get('user', default="", type=str)
    req_slug_id = args.get('slug', default="", type=str)

    if req_user_id == "" :
        return "bad user", 400
    
    if req_slug_id == "" :
        return "bad slug", 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT at FROM user_slug_states where "user_slug" = %s;', (req_user_id + "--" + req_slug_id,))
    user_slug_state = cur.fetchone()
    cur.close()
    conn.close()

    if user_slug_state == None:
        return "0", 200
    
    return str(user_slug_state[0]), 200


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8001)
    
    print("Server stopped.") 