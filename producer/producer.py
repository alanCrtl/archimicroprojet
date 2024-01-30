import time
import random
import socket
import hashlib
from kafka import KafkaProducer

NUM_PARTITIONS = 2

def generate_coordinate(start_lat, start_long):
    # Generate random latitude and longitude
    lat_delta = round(random.uniform(-1, 1), 6)
    long_delta = round(random.uniform(-1, 1), 6)

    lat = start_lat + lat_delta
    long = start_long + long_delta
    return round(lat, 6), round(long, 6)

def generate_message(lat, long):
    # Get the current date and time in ISO format
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")
    ip_address = socket.gethostbyname(socket.gethostname())
    return f'{lat}; {long}; {ip_address}; {current_date}'

def get_machine_partition():
    # Get the machine's IP address
    ip_address = socket.gethostbyname(socket.gethostname())
    print(f'IP: {ip_address}')
    # Use a hash function to generate a consistent hash value
    hash_value = int(hashlib.sha256(ip_address.encode()).hexdigest(), 16)

    # Calculate the partition based on the hash value
    partition = hash_value % NUM_PARTITIONS

    return partition

def delivery_report(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {}, partition: [{}]'.format(msg.topic(), msg.partition()))

def produce_messages(bootstrap_servers, topic, num_messages):
    producer_conf = {
        'bootstrap_servers': bootstrap_servers,
    }

    producer = KafkaProducer(**producer_conf)

    for _ in range(num_messages):
        lat, long = 43.321551, -0.359241  # start in Pau
        lat, long = generate_coordinate(lat, long)
        message = generate_message(lat, long)
        partition = get_machine_partition() or 0

        # Debug print statements
        print(f'Sending message: {message} to partition {partition}')

        producer.send(topic, value=message.encode(), partition=partition).add_callback(delivery_report)
        time.sleep(1)

    producer.flush()

if __name__ == '__main__':
    bootstrap_servers = 'kafka:9092'  # docker network inspect archimicroprojet_kafka_net
    topic = 'coordinates'
    num_messages = 30
    produce_messages(bootstrap_servers, topic, num_messages)

