create table watch_event (
    user varchar(100),
    slug varchar(100),
    at bigint,
    ts timestamp
) engine MergeTree order by ts;