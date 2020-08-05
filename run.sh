#!/usr/bin/env bash

docker run --hostname localhost -p 8080:5672 -p 15672:15672 rabbitmq &>/dev/null & disown;

pip install -r requirements.txt &>/dev/null &
python create_db &>/dev/null &
mkdir -p parser/content

sleep 30

echo Don\'t forget to kill all processes after work
echo and docker container rabbitmq
python -m flask run &>/dev/null &
echo Flask PID: $!
cd parser
python tasks_receiver.py &>/dev/null &
echo Parser PID: $!
