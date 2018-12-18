#!/usr/bin/env bash

while true
do
	echo "Triggering spark job"
	docker exec -it spark-master bin/spark-submit --master spark://spark-master:7077 --total-executor-cores 2 --executor-memory 512m /tmp/data/sparkScript.py
	sleep 1.5m
done
