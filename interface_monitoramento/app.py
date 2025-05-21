from flask import Flask, request, jsonify, render_template
import pika
from messages import add_message, get_messages
import threading

app = Flask(__name__)

broker = 'localhost'
port = 5672
queue_humidity = 'humidity_sensor'
queue_temperature = 'temperature_sensor'

def setup_rabbitmq_connection():
    """Configura a conexão com o RabbitMQ e inicia o consumo de mensagens"""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker, port=port, credentials=pika.PlainCredentials('admin', 'admin')))
    channel = connection.channel()
    
    channel.exchange_declare(exchange='sensor_data', exchange_type='topic')
    
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

rabbit_thread = threading.Thread(target=setup_rabbitmq_connection)
rabbit_thread.daemon = True
rabbit_thread.start()

@app.route('/messages', methods=['GET'])
def messages():
    return jsonify(get_messages())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/atuador/<nome>', methods=['POST'])
def controlar_atuador(nome):
    data = request.get_json()
    estado = data.get('estado')

    if nome not in ['light', 'fan'] or estado not in ['on', 'off']:
        return jsonify({'erro': 'Requisição inválida'}), 400

    # Publicar no RabbitMQ
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=broker,
            credentials=pika.PlainCredentials('admin', 'admin')
        ))
        channel = connection.channel()
        channel.exchange_declare(exchange='actuator_data', exchange_type='topic')

        routing_key = f'{nome}'
        if( estado == 'on'):
            estado = 'ON'
        else:
            estado = 'OFF'
        print(f"Publishing message: {routing_key} {estado}")
        channel.basic_publish(
            exchange='actuator_data',
            routing_key=routing_key,
            body=estado
        )
        connection.close()
        return jsonify({'status': f'{nome} {estado}'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)