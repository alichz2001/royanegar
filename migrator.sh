#!/bin/sh

# create clickhouse tables
migrate -path /migrations/clickhouse/ -database 'clickhouse://localhost:9000?username=royanegar_user&password=1234&database=default' -verbose up

# create postgres tables
migrate -path /migrations/postgresql/ -database postgres://royanegar_user:1234@localhost:5432/postgres?sslmode=disable -verbose up

# create kafka topics