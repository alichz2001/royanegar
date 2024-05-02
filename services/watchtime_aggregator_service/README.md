# Watchtime Aggregator Service

### this service is fully stateless and has only 2 responsibilities:
    - periodic run aggregation on events stored in clickhouse
    - and stream the result to kafka


# knonw issues:

managing periodic jobs is not best implemented and can be better.


