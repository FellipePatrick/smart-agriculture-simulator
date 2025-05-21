import pika
import threading
import time

class Actuator:
    def __init__(self, actuator_type):
        self.actuator_type = actuator_type
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host='localhost',
                credentials=pika.PlainCredentials('admin', 'admin')
            )
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='actuator_data', exchange_type='topic')
        self.channel.queue_declare(queue=self.queue_name(), durable=False)
        self.channel.queue_bind(
            exchange='actuator_data',
            queue=self.queue_name(),
            routing_key=self.queue_name()
        )
        self.channel.basic_consume(
            queue=self.queue_name(),
            on_message_callback=self.callback,
            auto_ack=True
        )
        print(f"Actuator {self.actuator_type} is ready to receive messages.")

    def queue_name(self):
        return self.actuator_type
    
    def callback(self, ch, method, properties, body):
        if self.actuator_type == "fan":
            print(f"Estado do ventilador: {body.decode() == 'ON'}")

        elif self.actuator_type == "light":
            print(f"Estado da luz: {body.decode() == 'ON'}")

    def start_consuming(self):
        thread = threading.Thread(target=self._consume, daemon=True)
        thread.start()
    
    def _consume(self):
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.connection.close()

if __name__ == "__main__":
    actuator_fan = Actuator("fan")
    actuator_light = Actuator("light")
    
    actuator_fan.start_consuming()
    actuator_light.start_consuming()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Desligando atuadores...")