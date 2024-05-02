import clickhouse_connect
import psycopg2
from threading import Thread
import datetime
from kafka import KafkaProducer


def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='postgres',
                            user='royanegar_user',
                            password='1234')
    return conn

def user_watchtimes_aggregator():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT last_aggregated_at FROM aggregator_worker_states where "id" = \'user_watchtimes_aggregator_worker\';')
    state = cur.fetchone()

    if state == None:
        now = datetime.datetime(2022, 1, 1, 0, 0, 0, 0)
        cur.execute('insert into aggregator_worker_states values (\'user_watchtimes_aggregator_worker\', %s) returning (last_aggregated_at)', (now,))
        state = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    start_timestamp = state[0]
    end_timestamp = start_timestamp + datetime.timedelta(minutes=10)

    do_aggregate_user_watchtimes(start_timestamp, end_timestamp)

# user_watchtimes_aggregator_worker = Thread(target=user_watchtimes_aggregator, args=(), daemon=True, name='Background')
# user_watchtimes_aggregator_worker.start()


def do_aggregate_user_watchtimes(start_timestamp, end_timestamp):
    sql = """
    with watch_time_cte as(
        SELECT "user",
            at,
            lagInFrame(at) OVER (PARTITION BY "user" ORDER BY ts) AS prev_at
        FROM watch_event
        -- where ts between %s and %s
    ), aggregated_data as (
        SELECT "user", SUM(if(prev_at <= 0 or prev_at > at, 0, at - prev_at)) AS total_watch_time
        FROM watch_time_cte
        GROUP BY "user"
    ) select * from aggregated_data
    where total_watch_time > 0;
    """

    client = clickhouse_connect.get_client(host='localhost', username='royanegar_user', password='1234')

    # resp = client.raw_stream(sql)

    # while True:
    #     print(resp.readline())

    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    future = producer.send("test", b"asdfadsf")

    try:
        record_metadata = future.get(timeout=10)
        print(record_metadata)
    except KafkaError:
        # Decide what to do if produce request failed...
        log.exception()
        pass

    producer.flush()
    









if __name__ == "__main__":

    user_watchtimes_aggregator()
