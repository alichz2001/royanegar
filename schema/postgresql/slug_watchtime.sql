create table if not exists slug_watchtime
(
    slug   varchar(100) primary key ,
    duration bigint
);
create index slug_watchtime_hash_index ON slug_watchtime USING hash (slug);