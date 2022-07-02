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

RUN mkdir -p /root/hdfs && \
    mkdir -p /root/avro

COPY config-hdfs/* /tmp/ 

RUN mv /tmp/start-connect.sh ~/ && \
    mv /tmp/connect-standalone.properties  $KAFKA_HOME/config/connect-standalone.properties && \
    mv /tmp/confluentinc-kafka-connect-hdfs3-1.1.12.zip  ~/hdfs/confluentinc-kafka-connect-hdfs3-1.1.12.zip && \
    unzip ~/hdfs/confluentinc-kafka-connect-hdfs3-1.1.12.zip -d ~/hdfs/ && \
    mv ~/hdfs/confluentinc-kafka-connect-hdfs3-1.1.12 ~/hdfs/plugins &&\
    rm  ~/hdfs/confluentinc-kafka-connect-hdfs3-1.1.12.zip 

RUN mv /tmp/quickstart-hdfs.properties ~/hdfs/plugins/etc 

RUN chmod +x ~/start-connect.sh


CMD [ "sh", "-c", "/root/start-connect.sh"]


  # # avro 
    # mv /tmp/confluentinc-kafka-connect-avro-converter-7.1.1.zip /root/avro/ && \
    # unzip ~/avro/confluentinc-kafka-connect-avro-converter-7.1.1.zip  -d ~/avro/ && \
    # rm /root/avro/confluentinc-kafka-connect-avro-converter-7.1.1.zip

