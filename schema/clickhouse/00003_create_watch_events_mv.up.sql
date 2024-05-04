
CREATE MATERIALIZED VIEW watch_events_mv TO watch_events AS
SELECT *
FROM watch_events_kafka_queue;
