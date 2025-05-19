from flask import Flask, request, jsonify, render_template
import paho.mqtt.client as mqtt
from messages import add_message, get_messages

app = Flask(__name__)

broker = 'localhost'
port = 15672
topic = 'test'

def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f'Received message: {msg.topic} {msg.payload.decode()}')
    add_message(msg.topic, msg.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)
client.loop_start()

@app.route('/messages', methods=['GET'])
def messages():
    return jsonify(get_messages())

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
