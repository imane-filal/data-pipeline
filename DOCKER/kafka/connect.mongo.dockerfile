FROM ubuntu:latest

LABEL maintainer = "@Red_One"
WORKDIR /root

RUN apt-get update && \
    apt-get install -y \
    openssh-server \
    openjdk-8-jdk \
    wget \
    nano \
    unzip

RUN wget https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz && \
    tar -xzvf kafka_2.13-3.1.0.tgz && \
    mv kafka_2.13-3.1.0 /usr/local/kafka && \
    rm kafka_2.13-3.1.0.tgz

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV KAFKA_HOME=/usr/local/kafka

RUN mkdir -p /root/mongo
COPY config-mongo/* /tmp/ 

RUN mv /tmp/start-connect.sh ~/ && \
    mv /tmp/connect-standalone.properties  $KAFKA_HOME/config/connect-standalone.properties && \
    mv /tmp/mongodb-kafka-connect-mongodb-1.7.0.zip  ~/mongo/mongodb-kafka-connect-mongodb-1.7.0.zip && \
    unzip ~/mongo/mongodb-kafka-connect-mongodb-1.7.0.zip -d ~/mongo/ && \
    mv ~/mongo/mongodb-kafka-connect-mongodb-1.7.0 ~/mongo/plugins &&\
    rm  ~/mongo/mongodb-kafka-connect-mongodb-1.7.0.zip


RUN mv /tmp/MongoSourceConnector.properties ~/mongo/plugins/etc && \
    mv /tmp/MongoSinkConnector.properties ~/mongo/plugins/etc && \
    mv /tmp/mongo-kafka-connect-1.7.0-all.jar ~/mongo/plugins/lib

RUN chmod +x ~/start-connect.sh


CMD [ "sh", "-c", "/root/start-connect.sh"]