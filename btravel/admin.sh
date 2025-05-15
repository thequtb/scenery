#!/bin/bash

case "$1" in
  "build")
    buildah from --name btravel-bld docker.io/python:3.11
    buildah run btravel-bld bash -c "apt update && apt upgrade -y && apt install -y postgresql-client"
    buildah commit btravel-bld btravel:latest
    ;;
  "run")
    podman run --name btravel-api --replace -d -p 8000:8000 -e DB_PASSWORD=bismillah -e DB_NAME=btravel -e DB_USER=qutb -e DB_HOST=db --network=scenery btravel-api:latest
    ;;
  "run-web")
    echo "Starting BTravel web frontend..."
    cd "$(dirname "$0")/web" && ./run.sh
    ;;
  *)
    echo "Usage: $0 {build|run|run-web}"
    exit 1
    ;;
esac