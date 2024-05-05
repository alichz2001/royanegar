import datetime

def get_worker_state(conn, worker_id):
    cur = conn.cursor()
    cur.execute('SELECT last_aggregated_at FROM aggregator_worker_states where "id" = %s;', (worker_id,))
    state = cur.fetchone()

    if state == None:
        initial_date = datetime.datetime(2022, 1, 1, 0, 0, 0, 0)
        cur.execute('insert into aggregator_worker_states values (%s, %s) returning (last_aggregated_at)', (worker_id, initial_date,))
        state = cur.fetchone()

    cur.close()
    return state
