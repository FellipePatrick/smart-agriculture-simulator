from flask import Flask, request, jsonify, render_template
import pika
from messages import add_message, get_messages
import threading

app = Flask(__name__)

# Configurações do RabbitMQ
broker = 'localhost'
port = 5672  # Porta padrão do AMQP
queue_humidity = 'humidity_sensor'
queue_temperature = 'temperature_sensor'

def setup_rabbitmq_connection():
    """Configura a conexão com o RabbitMQ e inicia o consumo de mensagens"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker, port=port, credentials=pika.PlainCredentials('admin', 'admin')))
    channel = connection.channel()
    
    # Declara a exchange (opcional, mas boa prática)
    channel.exchange_declare(exchange='sensor_data', exchange_type='topic')
    
    # Declara a fila
    channel.queue_declare(queue=queue_humidity, durable=False)
    channel.queue_bind(exchange='sensor_data', queue=queue_humidity, routing_key=queue_humidity)

    channel.queue_declare(queue=queue_temperature, durable=False)
    channel.queue_bind(exchange='sensor_data', queue=queue_temperature, routing_key=queue_temperature)
    
    def callback(ch, method, properties, body):
        """Callback chamado quando uma mensagem é recebida"""
        print(f"Received message: {method.routing_key} {body.decode()}")
        add_message(method.routing_key, body.decode())
    
    channel.basic_consume(queue=queue_temperature, on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue=queue_humidity, on_message_callback=callback, auto_ack=True)
    
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

# Inicia a conexão com RabbitMQ em uma thread separada
rabbit_thread = threading.Thread(target=setup_rabbitmq_connection)
rabbit_thread.daemon = True
rabbit_thread.start()

@app.route('/messages', methods=['GET'])
def messages():
    return jsonify(get_messages())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)