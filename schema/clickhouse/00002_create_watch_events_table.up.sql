create table if not exists watch_events (
    user varchar(100),
    slug varchar(100),
    at bigint,
    ts timestamp default now()
) engine MergeTree order by ts;