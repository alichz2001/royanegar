from conn import *
from worker_utils import *
import datetime

def aggregate():
    conn = get_pg_connection()
    id = "user_watchtimes_aggregator_worker"

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
    with cte_with_prev_at as (
        select
            "user",
            slug,
            at,
            ts,
            lagInFrame(at) over (partition by ("user", slug) order by ts) as prev_at,
            if(prev_at == 0 or prev_at > at, 0, at - prev_at) as duration
        from watch_events
    ), filter_date as(
        select * from cte_with_prev_at
        where ts between '%s' and '%s'
    ), aggregated_data as(
        select "user", sum(duration) as added_watchtime from filter_date
        group by ("user")
    )
    select * from aggregated_data
    where added_watchtime > 0
    format CSV;
    """ % (start_timestamp.strftime('%Y-%m-%d %H:%M:%S'), end_timestamp.strftime('%Y-%m-%d %H:%M:%S'))


    client = get_ch_connection()
    resp = client.raw_stream(sql)
    
    cur = conn.cursor()

    cur.execute("create temp table temp_user_watchtime (\"user\" varchar(100), duration int) on commit drop")
    with cur.copy("copy temp_user_watchtime from stdin CSV DELIMITER ','") as copy:
        copy.write(resp.data)

    cur.execute("""
    insert into user_watchtimes("user", duration)
    select "user" as user, sum(duration) from temp_user_watchtime
        group by ("user")
    on conflict ("user")
    do update set duration=excluded.duration + user_watchtimes.duration;
    """)

    cur.close()
    