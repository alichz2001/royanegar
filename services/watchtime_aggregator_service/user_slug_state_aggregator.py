from conn import *
from worker_utils import *
import datetime

def aggregate():
    conn = get_pg_connection()
    id = "user_slug_state_aggregator_worker"

    state = get_worker_state(conn, id)

    start_timestamp = state[0]
    end_timestamp = datetime.datetime.now()

    do_aggregate_user_watchtimes(conn, start_timestamp, end_timestamp)

    cur = conn.cursor()
    cur.execute('update aggregator_worker_states set last_aggregated_at = %s where id = %s;', (end_timestamp, id, ))
    cur.close()
    conn.commit()
    conn.close()

def do_aggregate_user_watchtimes(conn, start_timestamp, end_timestamp):
    sql = """
    select "user", slug, last_value(at)
    from watch_events
    where ts between '%s' and '%s'
    group by ("user", slug)
    format CSV;
    """ % (start_timestamp.strftime('%Y-%m-%d %H:%M:%S'), end_timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    client = get_ch_connection()
    resp = client.raw_stream(sql)
    
    cur = conn.cursor()

    cur.execute("create temp table temp_user_slug_state (\"user\" varchar(100), \"slug\" varchar(100), at int) on commit drop")
    with cur.copy("copy temp_user_slug_state from stdin CSV DELIMITER ','") as copy:
        copy.write(resp.data)

    cur.execute("""
    insert into user_slug_states("user_slug", at)
    select "user" || '--' || "slug" as user_slug, MAX(at) from temp_user_slug_state
        group by ("user", "slug")
    on conflict ("user_slug")
    do update set at=excluded.at;
    """)

    cur.close()
    