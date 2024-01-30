from confluent_kafka import Consumer, KafkaError
import psycopg2
from psycopg2 import sql
import requests
import httpx
"""
"""
class Coord:
    def __init__(self, lat, long, ip, date) -> None:
        self.lat: float = lat
        self.long: float = long
        self.ip: str = ip
        self.date: str = date


def push_to_db(coord: Coord):
    data = {
       'latitude' : coord.lat,
        'longitude' : coord.long,
        'date':coord.date,
        'ip': coord.ip
    }
    session = requests.Session()
    session.trust_env = False
   
    session.post('http://api:8000/coordonnees', json=data)
   
    
# ==== main functions ====
def consume_messages(bootstrap_servers, group_id, topic):
    consumer_conf = {
        'bootstrap.servers': bootstrap_servers,
        'group.id': group_id,
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe([topic])
    
    max_iterations_without_messages = 15
    iterations_without_messages = 0



    print(f'bootstrapped the consumer to broker and topic [{topic}]; waiting for messages...')
    try:
        while True:
            msg = consumer.poll(timeout=10)
            
            # exit after too much idle time
            if msg is None:
                iterations_without_messages += 1
                if iterations_without_messages > max_iterations_without_messages:
                    print("No messages received for {} iterations. Exiting.".format(max_iterations_without_messages))
                    break
                else:
                    print("No messages received. Iteration: {}".format(iterations_without_messages))
                continue

            iterations_without_messages = 0  # Reset the count when a message is received

            # error handling
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print("Reached end of partition. Continuing.")
                    continue
                else:
                    print("Error: {}".format(msg.error()))
                    break
            
            # parse message
            print(f'msg received: {msg.value().decode("utf-8")}')
            splitted_message = msg.value().decode('utf-8').split('; ')
            lat = float(splitted_message[0])
            long = float(splitted_message[1])
            ip = splitted_message[2]
            date = splitted_message[3]

            
            # turn it into object and push to DB
            coord = Coord(lat=lat, long=long, ip=ip, date=date)
            push_to_db(coord)
            
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        pass

    finally:
        print("Exiting the consumer.")
        consumer.close()

if __name__ == '__main__':
    bootstrap_servers = 'kafka:9092'  # Kafka broker's address
    group_id = 'my-consumer-group'
    topic = 'coordinates'
    consume_messages(bootstrap_servers, group_id, topic)