create table if not exists user_slug_states
(
    user_slug   varchar(201) primary key ,
    "time" bigint
);
create index user_slug_states_hash_index ON user_slug_states USING hash (user_slug);