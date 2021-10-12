import pika
from dotenv import load_dotenv
import json
import os

CHANNEL = None

load_dotenv() 
RABBIT_SERVER = os.getenv("RABBIT_SERVER")
RABBIT_PORT = os.getenv("RABBIT_PORT")
RABBIT_VHOST = os.getenv("RABBIT_VHOST")
RABBIT_USER = os.getenv("RABBIT_USER")
RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD")

TO_1C_EXCHANGE = os.getenv("TO_1C_EXCHANGE")
TO_1C_QUEUE = os.getenv("TO_1C_QUEUE")

def init():
    global CHANNEL
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PASSWORD)
    parameters = pika.ConnectionParameters(host=RABBIT_SERVER,
                                           port=RABBIT_PORT,
                                           credentials=credentials,
                                           virtual_host=RABBIT_VHOST)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    CHANNEL = channel

    # Определяем обменники
    channel.exchange_declare(exchange=TO_1C_EXCHANGE, exchange_type='fanout')

    # Определяем очереди
    channel.queue_declare(queue=TO_1C_QUEUE, durable=True)

    # Привязываем очереди к обменникам
    channel.queue_bind(queue=TO_1C_QUEUE, exchange=TO_1C_EXCHANGE)



def put_message(message):
    pass

if __name__ == '__main__':
    init()

    message = json.dumps({
        'some': 'sample',
        'test': True
    })

    put_message(message)

    print(message)