create table if not exists user_watchtimes
(
    "user"   varchar(100) primary key ,
    duration bigint
);
create index user_watchtimes_hash_index ON user_watchtimes USING hash ("user");