create table if not exists slug_watchtimes
(
    slug   varchar(100) primary key ,
    duration bigint
);
create index slug_watchtimes_hash_index ON slug_watchtimes USING hash (slug);