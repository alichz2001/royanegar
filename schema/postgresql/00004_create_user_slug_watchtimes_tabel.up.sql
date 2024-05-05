create table if not exists user_slug_watchtimes
(
    user_slug   varchar(201) primary key ,
    duration bigint
);
create index user_slug_watchtimes_hash_index ON user_slug_watchtimes USING hash (user_slug);