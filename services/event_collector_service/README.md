# Event Collector Service

### this service is fully stateless and has only 2 responsibility:
    - listen for events from any client
    - stream events to storage(clickhouse) in as efficient as possible way


this service is fully stateless and can scale in hosrizantal way. 

probable bottleneck in this service is count of live client connections that can handle by horizontal scaling.
