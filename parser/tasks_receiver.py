import pika
from utils import get_url_from_db, change_task_status
from custom_parser import parse_url
# docker run --hostname localhost -p 8080:5672 -p 15672:15672 rabbitmq:3-management


def do_task(ch, method, properties, body):
    task_id = body.decode("utf-8")
    url = get_url_from_db(task_id)
    print(" [x] Received %r" % task_id)
    if url:
        change_task_status(task_id, "parsing")
        parse_url(url)
        change_task_status(task_id, "parsed")
    else:
        print("Incorrect task_id {0}".format(task_id))


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 8080, '/', credentials))

channel = connection.channel()
channel.queue_declare(queue='parse_urls')

channel.basic_consume(queue='parse_urls', on_message_callback=do_task, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
