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

def generate_message(lat, long, ip):
    # Get the current date and time in ISO format
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    """
    if producer could work on different machine :
        ip_address = socket.gethostbyname(socket.gethostname())

    """
    return f'{lat}; {long}; {ip}; {current_date}'

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
    coor = [[51.071002,2.5245134], [43.321551, -0.359241], [48.9751103,8.1767166], [42.3332995,2.5277649], [48.111339 ,-1.6800198]]

    i = random.randint(0, 4)

    return coor[i][0], coor[i][1]

def go_paris(lat, long):
    i = random.random()*0.01

    if lat<48.8 : lat = lat+random.random()*0.01
    if lat>48.8 : lat = lat-random.random()*0.01
    if long<2.3 : long = long+random.random()*0.01
    if long>2.3 : long = long-random.random()*0.01

    return lat, long

#generate fake ip to simulate different machine producing
def generate_ip():
    i = random.randint(2, 255)

    return f'127.0.0.{i}'

def produce_messages(bootstrap_servers, topic, num_messages):
    producer_conf = {
        'bootstrap.servers': bootstrap_servers,
    }

    producer = Producer(producer_conf)
    producer_ip = generate_ip()

    lat, long = random_start()

    for _ in range(num_messages):
        lat, long = go_paris(lat, long)
        message = generate_message(lat, long, producer_ip)
        partition = get_machine_partition() or 0

        # Debug print statements
        print(f'Sending message: {message} to partition {partition}')

        producer.produce(topic, value=message, partition=partition, callback=delivery_report)

        time.sleep(0.5)


    producer.flush()

if __name__ == '__main__':
    bootstrap_servers = 'kafka:9092'  # docker network inspect archimicroprojet_kafka_net
    topic = 'coordinates'
    num_messages = 300
    produce_messages(bootstrap_servers, topic, num_messages)

