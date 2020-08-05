# Simple API with Flask

API with two main methods using flask:
1. [POST] the request receives the URL and returns the task ID in response
1. [GET]  the request receives the task ID and returns the current state of the task. When the task is completed, it returns the URL where the archive can be downloaded.

### The task performed by:

The parser that runs through the site with limited nesting (default - 2) and saves html/css/js and media files to an archive.

## Running
Create a virtual python environment and activate it. And just run run.sh:
```sh
run.sh
```
or for Windows
```sh
bash run.sh
```
Go to http://localhost:5000/

# How it works

Flask receives new URL and adds a task to the sqlite database, and returns the ID of the task for parsing this URL to you. And sends the new job to the RabbitMQ queue.

The parser runs separately. Receives a new job from the RabbitMQ queue and starts work.

Each stage is displayed in the task status in the database.
