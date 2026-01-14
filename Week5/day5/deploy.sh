#!/bin/bash

echo "Stopping existing containers..."
docker compose -f docker-compose.prod.yml down

echo "Building images..."
docker compose -f docker-compose.prod.yml build

echo "Starting application in detached mode..."
docker compose -f docker-compose.prod.yml up -d

echo "Deployment completed successfully"

