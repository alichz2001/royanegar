create table if not exists aggregator_worker_states (
    id varchar(100) primary key,
    last_aggregated_at timestamp
)