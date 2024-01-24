from kafka import KafkaConsumer
import psycopg2
from psycopg2 import sql

class Coord:
    def __init__(self, lat, long, ip, date) -> None:
        self.lat: float = lat
        self.long: float = long
        self.ip: str = ip
        self.date: str = date
    
def connect_to_db():
    dbname = "coords"
    user = "root"
    password = "password"
    host = "postgres"
    port = "5432"
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return connection

def push_to_db(coord: Coord):
    connection = connect_to_db()

    try:
        with connection.cursor() as cursor:
            insert_query = sql.SQL("""
                INSERT INTO coordonnee (lat, long, ip, date)
                VALUES (%s, %s, %s, %s)
            """)
            cursor.execute(insert_query, (coord.lat, coord.long, coord.ip, coord.date,))

        connection.commit()

    finally:
        connection.close()
    return {"status": "Message pushed to the database successfully"}

def clear_db():
    connection = connect_to_db()

    try:
        with connection.cursor() as cursor:
            delete_query = sql.SQL("""
                DELETE FROM coordonnee
            """)
            cursor.execute(delete_query)

        connection.commit()

    finally:
        connection.close()
    
    return {"status": "All rows cleared from the database"}
    
def get_column_names():
    connection = connect_to_db()

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'coordonnee';")
            column_names = cursor.fetchall()

        return [column[0] for column in column_names]

    finally:
        connection.close()

# ==== main functions ====
# ==== main functions ====
def consume_messages(bootstrap_servers, group_id, topic):

    consumer_conf = {
        'bootstrap_servers': bootstrap_servers,
        'group_id': group_id,
        'enable_auto_commit': True
    }

    consumer = KafkaConsumer(topic, **consumer_conf)
    consumer.subscribe([topic])
    
    max_iterations_without_messages = 5
    iterations_without_messages = 0

    # connect to database and show column names
    column_names = get_column_names()
    print("DB Column Names:", column_names)

    try:
        while True:
            print('waiting for messages...')
            messages = consumer.poll(timeout_ms=4000)
            
            if not messages:
                iterations_without_messages += 1
                print('No messages received.')
                if iterations_without_messages > max_iterations_without_messages:
                    print("No messages received for {} iterations. Exiting.".format(max_iterations_without_messages))
                    break
                else:
                    print("No messages received. Iteration: {}".format(iterations_without_messages))
                continue

            iterations_without_messages = 0  # Reset the count when a message is received
            
            for topic_partition, partition_messages in messages.items():
                for msg in partition_messages:
                    process_kafka_message(msg)

    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        pass

    finally:
        print("Exiting the consumer.")
        consumer.close()

def process_kafka_message(msg):
    try:
        # parse message
        print(f'msg received: {msg.value.decode("utf-8")}')
        splitted_message = msg.value.decode('utf-8').split(';')
        lat = float(splitted_message[0])
        long = float(splitted_message[1])
        ip = splitted_message[2]
        date = splitted_message[3]

        # turn it into object and push to DB
        coord = Coord(lat=lat, long=long, ip=ip, date=date)
        print(f'coord : {coord}')
        push_to_db(coord)

    except Exception as e:
        print(f"Error processing message: {e}")

if __name__ == '__main__':
    print('hello from consumer')
    bootstrap_servers = 'kafka:9093'  # Kafka broker's address
    group_id = 'my-consumer-group'
    topic = 'coordinates'
    consume_messages(bootstrap_servers, group_id, topic)