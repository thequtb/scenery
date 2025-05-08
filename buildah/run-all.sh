#!/bin/bash
# Run all buildah scripts in the correct order

set -e  # Exit on error

echo "Creating network..."
podman network exists plugnet || podman network create plugnet

echo "Building and running Redis..."
bash redis.sh

echo "Building and running PostgreSQL..."
bash psql.sh

echo "Building and running Spark (Telegram webhook service)..."
bash spark.sh

echo "Building and running Journal (Phoenix API)..."
bash journal.sh

echo "All services deployed successfully!"
echo "Spark webhook available at: http://localhost:8080/webhook/telegram"
echo "Journal API available at: http://localhost:4000" 