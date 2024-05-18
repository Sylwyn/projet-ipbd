#!/bin/bash

echo "copying data to druid"

# if there's no argument, ask the user for the path to the data or it's empty
if [$# -eq 0]; then
    echo "Please provide the path to the data"
    read path
else
    path=$1
fi

for docker in broker middlemanager router historical coordinator ; do
    docker cp $path $docker:/opt/druid/quickstart 
done

echo "data copied to druid"