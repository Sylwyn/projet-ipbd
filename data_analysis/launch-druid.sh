#!/bin/bash

echo "launching druid"
docker compose -f ./druid/distribution/docker/docker-compose.yml up -d

