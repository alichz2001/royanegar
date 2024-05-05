#!/bin/sh

# create clickhouse tables
clickhouse_conn_str="clickhouse://${DB_CH_HOSTNAME}:9000?username=${DB_CH_USER}&password=${DB_CH_PASSWORD}&database=${DB_CH_DATABASE_NAME}"
migrate -path /migrations/clickhouse/ -database ${clickhouse_conn_str} -verbose up

# create postgres tables
postgres_conn_str="postgres://${DB_PG_USER}:${DB_PG_PASSWORD}@${DB_PG_HOST}:${DB_PG_PORT}/${DB_PG_DATABASE_NAME}?sslmode=disable"
migrate -path /migrations/postgresql/ -database ${postgres_conn_str} -verbose up
