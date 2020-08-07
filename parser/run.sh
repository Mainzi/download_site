#!/usr/bin/env bash
while !</dev/tcp/$POSTGRES_HOST/$POSTGRES_PORT; do sleep 10; done;
while !</dev/tcp/$RABBITMQ_URL/$RABBITMQ_PORT; do sleep 10; done;

cd flask_app
python -m flask run &>/dev/null &
cd ../parser
python tasks_receiver.py