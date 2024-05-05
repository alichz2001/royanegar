
# Roya Negar Task

---


## up and run

```
make up
```


## API doc

postman


## bottlenecks:

- live concurrent event publisher.
- aggregating so many events in a psudo-live manner.
- store watchtime data for high concurrent read.

## Tools

#### ClickHouse

- where it used? 
	- for storing events in disk and aggregate psudo-live data from events.
- why clickhouse?
    - we need some characteristic for storage of this data:
        1. high throughput
        2. efficiency in aggregating data
        3. support scaling, partitioning, backing up of data
        4. rich support for streaming to and from data to prevent memory peak in services.
        5. supporting integration with other tools like kafka

### PostgreSQL
	 
- where it used? 
	- for storing aggregated data for end-user. as key-value store
- why clickhouse?
    - we need some characteristic for storage of this data:
        1. consistency
        2. efficient index for fast retrieval data (hash index)
        3. support scaling, partitioning, backing up of data
        4. support efficient 'upsert' data for atomic update so many data.


### kafka

- where it used? 
	- for queuing and storing events.
- why clickhouse?
    - we need some characteristic for storage of this data:
        1. high throughput
        2. durability of data
        3. support scaling, partitioning of data
        4. efficient handling of buffers.
        

### notes

##### Event publishing protocol 
HTTP is not best choice for client event sending protocol. because of HTTP protocol overhead(useless headers in every published event).
for this problem maybe websocket or any other application layer protocols with less overhead is better choice.
##### Events encoding 
JSON is not best choice for encoding protocol because of encoding and decoding overhead and many useless metadata and characters. messagepack or protobuf or even CSV are better options.
