import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

teste = {
    "id":123,
    "status":'processando'
}

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=json.dumps(teste, indent = 4))
print(" [x] Sent 'Hello World!'")
connection.close()