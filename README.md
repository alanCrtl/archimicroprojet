# archi micro projet

# Table of Contents

- [Schema of Structure of Services](#schema-of-structure-of-services)
- [Gif of Running All Services](#gif-of-running-all-services)
- [Docker](#docker)
  - [Run Kafka](#run-kafka)
  - [Run PostgreSQL DB](#run-postgresql-db)
  - [Run API/Frontend Docker-Compose](#run-apifrontend-docker-compose)
  - [Run Consumer Docker-Compose](#run-consumer-docker-compose)
  - [Run Producer Docker-Compose](#run-producer-docker-compose)
  - [Useful Docker Commands for Debug](#useful-docker-commands-for-debug)
- [Old Documentation (No Docker)](#the-following-sections-are-old-documentation-for-running-things-manually-no-docker-kept-as-archive)
- [Kafka](#kafka)
  - [Data Format Sent to Topic Coordinates](#data-format-sent-to-topic-coordinates)
  - [Launch Broker on 2 Terminal (Go into Kafka Folder First)](#launch-broker-on-2-terminal-go-into-kafka-folder-first)
  - [Some Commands If It Fails (Go into Kafka Folder)](#some-command-if-it-fails-go-into-kafka-folder)
  - [Test Messages on 'test-topic'](#test-messages-on-test-topic)
  - [Create Topic Coordinates (One Time Only)](#create-topic-coordinates-one-time-only)
  - [Delete Topic](#delete-topic)
  - [List Topics](#list-topics)
  - [Kafka Server Logs](#kafka-server-logs)
  - [Broker Config (in server.properties)](#broker-config-in-serverproperties)
- [Database PostgreSQL](#database-postgresql)
  - [Create Super User for PostgreSQL](#create-super-user-for-postgresql)
  - [Create Empty Database and Restore the Database into the Empty One](#create-empty-database-and-restore-the-database-into-the-empty-one)
- [API](#api)
  - [Run API Manually](#run-api-manually)
- [Auteurs](#auteurs)



## Docker (ran with Docker version 25.0.0)

Go into docker/ and then enter these commands to run services

### Run kafka
```
docker-compose -f kafka-docker-compose.yml up --build
```

### Run the postgreSQL db
```
docker-compose -f bdd-docker-compose.yml up --build
```

### Run the api/frontend docker-compose
```
docker-compose -f api-docker-compose.yml up --build
```

### Run the consumer docker-compose
```
docker-compose -f docker-compose-consumer.yml up --build
```

### Run the producer docker-compose
```
docker-compose -f producer-docker-compose.yml up --build
```

**Once all services are running you can find the frontend(map) here : http://0.0.0.0:8000**


### useful docker commands for debug
*show containers*
```
docker ps
```
*restart service*
```
sudo service docker restart

```
*Stop a container (example)*
```
docker compose -f bdd-docker-compose.yml down
```
*reset networks*
```
docker network prune
```
*list process that use port*
```
sudo lsof -i :<PORT>
```
*hard reset*
```
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker rmi $(docker images -q)
docker volume rm $(docker volume ls -q)
docker network rm $(docker network ls -q)
docker system prune -a --volumes
```

## The following sections are old documentation for running things manually (no docker), kept as archive

## Kafka

[kafka quickstart guide](https://kafka.apache.org/quickstart)

### Data format sent to topic coordinates

The data is to the broker in the format: lat; long; Date; ip.<br>
Example: "-48.744897; -78.637573; 2023-12-27 16:03:41; 172.17.9.135"<br>

### launch broker on 2 terminal (go into kafka folder first)
```
bin/zookeeper-server-start.sh config/zookeeper.properties
```
```
bin/kafka-server-start.sh config/server.properties
``` 

### some command if it fails (go into kafka folder)

i needed to do this to install kafka i guess after cloning repo 

    ./gradlew jar -PscalaVersion=2.13.11

### test messages on 'test-topic'

write: 

    bin/kafka-console-producer.sh --topic test-topic --bootstrap-server localhost:9092

read: 

    bin/kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server localhost:9092

### create topic coordinates (one time only):

    bin/kafka-topics.sh --create --topic coordinates --bootstrap-server localhost:9092 --partitions 2 --replication-factor 1

### delete topic

	bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic coordinates

### list topics

	kafka-topics.sh --bootstrap-server localhost:9092 --list --command-config /path/to/client.properties
	
### kafka server logs:
    
    tail -f logs/server.log

### broker config (in server.properties):

    listeners=PLAINTEXT://localhost:9092
    
## Database POSTGRESQL

Once postgres installed (read requirements.txt)<br>
go into folder BDD/, and type ```createdb coords```<br>
if error : "role 'name' does not exist" then create a superuser
by following instructions below and by replacing cytech by
your name.
(to display users: once you type psql type \du)

### create super user for postgresql

    sudo -i -u postgres
    psql
    CREATE USER cytech WITH SUPERUSER CREATEDB CREATEROLE PASSWORD 'password';
    exit
    exit

### create empty database and restore the database into the empty one

    createdb -U cytech coords
    psql -U cytech -d coords -f db_microarchie.dump

## API 

### run api manually
```
uvicorn api:app --reload
```

# AUTEURS 

Aurelien CHAUVEHEID


# AUTEURS 

Aurelien CHAUVEHEID

Alan COURTEL

Ameilie LEANG

Marieme SALL
