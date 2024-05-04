create table if not exists watch_events_kafka_queue (
    user varchar(100),
    slug varchar(100),
    at bigint
) engine Kafka() settings
    kafka_broker_list = 'localhost:9092',
    kafka_topic_list = 'watch_events',
    kafka_group_name = 'clickhouse_watch_events_consumer',
    kafka_format = 'CSV',
    kafka_thread_per_consumer = 1,
    kafka_num_consumers = 1,
    kafka_client_id = 'clickhouse-001';



