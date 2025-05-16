#!/bin/bash

case "$1" in
  "build")
    buildah from --name btrvadm docker.io/python:3.12-slim

    buildah run btrvadm bash -c "apt update && apt upgrade -y"

    buildah config --workingdir /app/ btrvadm
    buildah copy btrvadm api/adm .
    buildah run btrvadm pip install --upgrade pip --root-user-action=ignore
    buildah run btrvadm pip install -r requirements.txt --root-user-action=ignore
    buildah run btrvadm python manage.py collectstatic --noinput
    buildah run btrvadm mv staticfiles static/

    buildah copy btrvadm entrypoint.sh .
    buildah config --entrypoint '["/app/entrypoint.sh"]' btrvadm
    buildah commit btrvadm btravel-admin:latest

    ;;
  "update")
    buildah copy btrvadm api/adm .
    buildah run btrvadm pip install -r requirements.txt --root-user-action=ignore
    buildah commit btrvadm btravel-admin:latest

    ;;
  "run")
    podman run --name btravel-admin --replace -d -p 8000:8000 -e DB_PASSWORD=bismillah -e DB_NAME=btravel -e DB_USER=qutb -e DB_HOST=db --network=scenery btravel-admin:latest
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