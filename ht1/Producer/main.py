import pika

try:
	connection = pika.BlockingConnection(
		pika.URLParameters("amqp://guest:guest@rabbitmq:5672")
	)
	channel = connection.channel()
	channel.queue_declare(queue='msgQ')

	while True:
		message = input()
		channel.basic_publish(exchange='', routing_key='messages',
								body=message.encode())
except KeyboardInterrupt:
	pass
except Exception as e:
	print(e)
	exit(1)
finally:
	connection.close()
