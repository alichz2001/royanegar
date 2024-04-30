create table if not exists user_watchtime
(
    user   varchar(100) primary key ,
    duration bigint
);
create index user_watchtime_hash_index ON user_watchtime USING hash (user);