create table if not exists user_slug_watchtime
(
    user_slug   varchar(201) primary key ,
    duration bigint
);
create index user_slug_watchtime_hash_index ON user_slug_watchtime USING hash (user_slug);