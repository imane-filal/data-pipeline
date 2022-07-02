#!/bin/bash

echo -e "\n"

$KAFKA_HOME/bin/connect-standalone.sh $KAFKA_HOME/config/connect-standalone.properties /root/hdfs/plugins/etc/quickstart-hdfs.properties 
# $KAFKA_HOME/bin/connect-distributed.sh $KAFKA_HOME/config/connect-distributed.properties /root/hdfs/plugins/etc/quickstart-hdfs.properties

echo -e "\n"



