#!/bin/bash

echo "extracting data to druid"

for docker in broker middlemanager router historical coordinator ; do
    docker exec -it $docker tar xf /opt/druid/quickstart/random_data_onelined_parsed.json.gz
done

echo "data extracted to druid"
