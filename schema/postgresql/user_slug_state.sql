create table if not exists user_slug_state
(
    user_slug   varchar(201) primary key ,
    "time" bigint
);
create index user_slug_state_hash_index ON user_slug_state USING hash (user_slug);