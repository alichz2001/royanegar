# Roya Negar Task

---



bottlenecks:

- live concurrent users that sent event.

### notes

- 'Events protocol' HTTP is not best choice for client event sending protocol. becouse of HTTP protocol itsel overhead(useless headers in every published event).
for this problem maybe websocket or any other application layer protocols with less overhead is better choice.
- 'Events encoding', JSON is not best choice for encoding protocl becouse of encoding and decoding overhead and many useless metadata. messagepack or protobuf or even CSV are better options.


### Tools

#### ClickHouse
'where it used?' for storing events in disk and aggregate psudo-live data from events.
'why clickhouse?' 
    - we need some characteristic for storage of this data:
        1. high throuput
        2. efficiency in aggregationing data
        3. suppurt scaling, partitioning, backuping of data
        4. rich support for streaing to and from data to prevent memmory peack in services.
        





https://clickhouse.com/docs/en/guides/inserting-data#insert-large-batches
https://clickhouse.com/docs/en/operations/settings/settings#async-insert

https://clickhouse.com/docs/en/integrations/python#client-raw_insert-method