import pika
import os


def send_task(task_id):
    # TODO: take out connection control and queue_declare
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(pika.ConnectionParameters(os.environ.get('RABBITMQ_URL') or 'localhost',
                                                                   os.environ.get('RABBITMQ_PORT') or 8080, '/',
                                                                   credentials))
    channel = connection.channel()

    channel.queue_declare(queue='parse_urls')
    channel.basic_publish(exchange='', routing_key='parse_urls', body=task_id)
    connection.close()
