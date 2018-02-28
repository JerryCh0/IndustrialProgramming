import pika
import psycopg2
import psycopg2.extras
import sys
import time


#--------------Deal with Database-------------
def db_init(cursor):
	cursor.execute('''
		CREATE TABLE IF NOT EXISTS
		messages(id SERIAL PRIMARY KEY,
			     message TEXT NOT NULL,
		         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL);''')

def db_insert(cursor, message):
	cursor.execute('''INSERT INTO messages (message) VALUES (%s);''', (message,))


#--------------Connecting the dots-------------
try:

	db_connection = psycopg2.connect(host="postgres", dbname="messages",
	user="user", password="password")

	db_connection.autocommit = True
	db_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
	db_init(db_cursor)

	db_cursor.execute('''SELECT COUNT(*) as count FROM messages;''')
	messages_count = db_cursor.fetchone()["count"]

	print("Have {} messages in database".format(messages_count))

	rabbit_connection = pika.BlockingConnection(
		pika.URLParameters("amqp://guest:guest@rabbitmq:5672")
	)

	rabbit_channel = rabbit_connection.channel()
	rabbit_channel.queue_declare(queue='messages')

	print("Ready for listening!")
	sys.stdout.flush()
	def callback(ch, method, properties, body):
		try:

			message = body.decode()
			db_insert(db_cursor, message)

			print("[x] {}".format(message))
			sys.stdout.flush()
		except Exception as e:
			print(e)
			sys.stdout.flush()

	rabbit_channel.basic_consume(callback, queue='messages', no_ack=True)
	rabbit_channel.start_consuming()

except Exception as e:
	print(e)
	exit(1)
finally:
	db_cursor.close()
	db_connaction.close()

	rabbit_connection.stop()
