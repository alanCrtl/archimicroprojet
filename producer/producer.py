import time
import random
import socket
import hashlib
from confluent_kafka import Producer

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


def random_start():
    coor = [[51.071002,2.5245134], [43.321551, -0.359241], [48.9751103,8.1767166], [42.3332995,2.5277649], [48.4140251,-4.7942741]]

    i = random.randint(0, 4)

    return coor[i][0], coor[i][1]

def go_paris(lat, long):
    if lat<48.9 and lat>48.7 and long<2.4 and long>2.2 :
        lat, long = random_start()

    if lat<48.8 : lat = lat+0.05
    if lat>48.8 : lat = lat-0.05
    if long<2.3 : long = long+0.05
    if long>2.3 : long = long-0.05

    return lat, long

def produce_messages(bootstrap_servers, topic, num_messages):
    producer_conf = {
        'bootstrap.servers': bootstrap_servers,
    }

    producer = Producer(producer_conf)

    lat, long = random_start()

    for _ in range(num_messages):
        lat, long = go_paris(lat, long)
        message = generate_message(lat, long)
        partition = get_machine_partition() or 0

        # Debug print statements
        print(f'Sending message: {message} to partition {partition}')

        producer.produce(topic, value=message, partition=partition, callback=delivery_report)


    producer.flush()

if __name__ == '__main__':
    bootstrap_servers = 'kafka:9092'  # docker network inspect archimicroprojet_kafka_net
    topic = 'coordinates'
    num_messages = 500
    produce_messages(bootstrap_servers, topic, num_messages)

