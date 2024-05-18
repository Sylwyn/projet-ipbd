#!/bin/bash
echo "launching superset"
docker compose -f ./superset/docker-compose-non-dev.yml up -d


