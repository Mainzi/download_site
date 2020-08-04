import functools
import threading
import pika

from utils import get_url_from_db, change_task_status
from custom_parser import parse_url


# docker run --hostname localhost -p 8080:5672 -p 15672:15672 rabbitmq:3-management


def do_task(body):
    task_id = body.decode("utf-8")
    url = get_url_from_db(task_id)
    print(" [x] Received %r" % task_id)
    if url:
        change_task_status(task_id, "parsing")
        parse_url(url, task_id)
        change_task_status(task_id, "parsed")
    else:
        print("Incorrect task_id {0}".format(task_id))


def ack_message(ch, delivery_tag):
    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        pass


def do_work(conn, ch, delivery_tag, body):
    do_task(body)

    cb = functools.partial(ack_message, ch, delivery_tag)
    conn.add_callback_threadsafe(cb)


def on_message(ch, method_frame, _header_frame, body, args):
    (conn, thrds) = args
    delivery_tag = method_frame.delivery_tag
    t = threading.Thread(target=do_work, args=(conn, ch, delivery_tag, body))
    t.start()
    thrds.append(t)


credentials = pika.PlainCredentials('guest', 'guest')

parameters = pika.ConnectionParameters('localhost', 8080, '/', credentials=credentials, heartbeat=5)
connection = pika.BlockingConnection(parameters)

channel = connection.channel()
channel.exchange_declare(
    exchange="test_exchange",
    exchange_type="direct",
    passive=False,
    durable=True,
    auto_delete=False)
channel.queue_declare(queue="parse_urls")
channel.queue_bind(queue="parse_urls", exchange="test_exchange", routing_key="standard_key")

# prefetch_count ~ the number of threads
channel.basic_qos(prefetch_count=2)

threads = []
on_message_callback = functools.partial(on_message, args=(connection, threads))
channel.basic_consume('parse_urls', on_message_callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# Wait for all to complete
for thread in threads:
    thread.join()

connection.close()
