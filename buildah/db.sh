#!/bin/bash

case "$1" in
  "build")
    buildah from --name db-bld docker.io/postgres:17.4
    buildah run db-bld bash -c "apt update && apt upgrade -y && apt install -y postgresql-17-pgvector"
    buildah copy db-bld pg-init/init.sql /docker-entrypoint-initdb.d/init.sql
    buildah commit db-bld db:latest
    ;;
  "run")
    podman run --name db --replace -d -p 5432:5432 -e POSTGRES_PASSWORD=bismillah -e POSTGRES_DB=btravel -e POSTGRES_USER=qutb --network=scenery db:latest
    ;;
  *)
    echo "Usage: $0 [build|run]"
    exit 1
    ;;
esac