# archi micro projet

## kafka broker
TODO:

idea: 
producer -> produce request to websocket -> websocket produce on the 'server' machine
the 'server' machine has a consumer which can consume the messages and put them 
in db.

[kafka quickstart guide](https://kafka.apache.org/quickstart)

### launch broker on 2 terminal:
    
    bin/zookeeper-server-start.sh config/zookeeper.properties
    
    bin/kafka-server-start.sh config/server.properties

### test messages on 'test-topic'

write: 

    bin/kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092

read: 

    bin/kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server localhost:9092

### create topic coordinates (one time only):

    bin/kafka-topics.sh --create --topic coordinates --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1

### delete topic

	bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic coordinates

### kafka server logs:
    
    tail -f logs/server.log

### broker config (in server.properties):

    listeners=PLAINTEXT://localhost:9092
