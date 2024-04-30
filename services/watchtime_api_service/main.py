import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='royanegar_user',
                            password='1234')
    return conn


@app.route('/api/v1/watchtime/user')
def user_watchtime():
    args = request.args
    req_user_id = args.get('id', default="", type=str)

    if req_user_id == "" :
        return "bad username", 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT duration FROM user_watchtimes where "user" = %s;', (req_user_id,))
    user_watchtime = cur.fetchone()
    cur.close()
    conn.close()

    if user_watchtime == None:
        return "0", 200
    
    return str(user_watchtime[0]), 200


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8001)
    
    print("Server stopped.") 