import pika
import random
import time

class Sensor:
    def __init__(self, sensor_type):
        self.sensor_type = sensor_type
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=pika.PlainCredentials('admin', 'admin')))
        self.channel = self.connection.channel()

    def send_data(self):
        self.channel.queue_declare(queue=self.queue_name())
        data = self.get_data_sensor()
        self.channel.basic_publish(exchange='sensor_data',
                                    routing_key=self.queue_name(),
                                    body=str(data))
        print(f" [x] Sent {data} to {self.sensor_type}")
        self.connection.close()

    def queue_name(self):
        return self.sensor_type
    
    def get_data_sensor(self):
        if self.sensor_type == "temperature_sensor":
            return round(random.uniform(28.0, 40.0),2)
        elif self.sensor_type == "humidity_sensor":
            return round(random.uniform(30.0, 70.0),2)


if __name__ == "__main__":

    sensor_types = ["temperature_sensor", "humidity_sensor"]        
    while True:
        sensor_type = random.choice(sensor_types)
        sensor = Sensor(sensor_type)
        sensor.send_data()
        time.sleep(2)