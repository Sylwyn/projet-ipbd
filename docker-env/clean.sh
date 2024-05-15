#/bin/bash

# stopping docker
echo "stopping the docker"
docker stop $(docker ps -a -q)
echo "deleting the docker"
docker rm $(docker ps -a -q)

