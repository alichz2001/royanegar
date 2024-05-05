from conn import *
from worker_utils import *
import datetime

def aggregate():
    conn = get_pg_connection()
    id = "user_slug_watchtimes_aggregator_worker"

    state = get_worker_state(conn, id)

    start_timestamp = state[0]
    end_timestamp = datetime.datetime.now()

    do_aggregate_user_slug_watchtimes(conn, start_timestamp, end_timestamp)

    cur = conn.cursor()
    cur.execute('update aggregator_worker_states set last_aggregated_at = %s where id = %s;', (end_timestamp, id, ))
    cur.close()
    conn.commit()
    conn.close()

def do_aggregate_user_slug_watchtimes(conn, start_timestamp, end_timestamp):
    sql = """
    with cte_with_prev_at as (
        select
            "user",
            slug,
            at,
            lagInFrame(at) over (partition by ("user", slug) order by ts) as prev_at,
            if(prev_at == 0 or prev_at > at, 0, at - prev_at) as duration
        from watch_events
        where ts between '%s' and '%s'
    ), aggregated_data as(
        select user, slug, sum(duration) as added_watchtime from cte_with_prev_at
        group by (user, slug)
    )
    select * from aggregated_data
    where added_watchtime > 0
    format CSV;
    """ % (start_timestamp.strftime('%Y-%m-%d %H:%M:%S'), end_timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    client = get_ch_connection()
    resp = client.raw_stream(sql)
    
    cur = conn.cursor()

    cur.execute("create temp table temp_user_slug_watchtime (\"user\" varchar(100), slug varchar(100), duration int) on commit drop")
    with cur.copy("copy temp_user_slug_watchtime from stdin CSV DELIMITER ','") as copy:
        copy.write(resp.data)

    cur.execute("""
    insert into user_slug_watchtimes(user_slug, duration)
    select "user" || '--' || slug as user_slug, sum(duration) from temp_user_slug_watchtime
        group by ("user", slug)
    on conflict (user_slug)
    do update set duration=excluded.duration + user_slug_watchtimes.duration;
    """)

    cur.close()
    