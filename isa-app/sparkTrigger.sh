#!/usr/bin/env bash
echo "Installing packages...."

apt-get update
apt-get install python3-dev libmysqlclient-dev -y
apt-get install python-pip -y
pip install mysqlclient
apt-get install python-mysqldb

while true
do
	echo "Triggering spark job"
	docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/sparkScript.py
	sleep (2 * 60 * 1000)
done
