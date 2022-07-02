#!/bin/bash

echo -e "\n"

$KAFKA_HOME/bin/connect-standalone.sh $KAFKA_HOME/config/connect-standalone.properties /root/mongo/plugins/etc/MongoSourceConnector.properties

echo -e "\n"



