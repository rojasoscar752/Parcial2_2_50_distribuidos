import pika
import json
import os

def callback(ch, method, properties, body):
    message = json.loads(body)
    with open("/data/messages.log", "a") as f:
        f.write(json.dumps(message) + "\n")
    print("Mensaje guardado:", message)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="messages", durable=True)
    channel.basic_consume(queue="messages", on_message_callback=callback, auto_ack=True)
    print("Esperando mensajes...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
