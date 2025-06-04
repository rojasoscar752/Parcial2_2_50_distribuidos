import pika
import json
import time

def connect_to_rabbitmq(retries=5, delay=3):
    for i in range(retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
            return connection
        except pika.exceptions.AMQPConnectionError:
            print(f"[Intento {i+1}] RabbitMQ no disponible, reintentando en {delay} segundos...")
            time.sleep(delay)
    raise Exception("No se pudo conectar a RabbitMQ después de varios intentos")

def callback(ch, method, properties, body):
    message = json.loads(body)
    with open("/data/messages.log", "a") as f:
        f.write(json.dumps(message) + "\n")
    print("Mensaje guardado:", message)

def main():
    connection = connect_to_rabbitmq()
    channel = connection.channel()
    channel.queue_declare(queue="messages", durable=True)
    channel.basic_consume(queue="messages", on_message_callback=callback, auto_ack=True)
    print("Esperando mensajes...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
