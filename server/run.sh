#!/usr/bin/env bash
while !</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT; do sleep 10; done;
while !</dev/tcp/$RABBITMQ_URL/$RABBITMQ_PORT; do sleep 10; done;

python -m flask run