SHELL := /bin/bash

ENV_FILE := ./.env

include $(ENV_FILE)

export
.PHONY: setup up down restart

test: 
	@echo ${DB_CH_PORT}

up: setup
	@echo "Starting Docker Compose..."
	docker-compose -f ./docker-compose.yaml up --build --force-recreate
	@echo "Docker Compose is up and running."

down:
	@echo "Stopping Docker Compose..."
	@docker-compose -f ./docker-compose.yaml down
	@echo "Docker Compose is stopped."

restart: down up
