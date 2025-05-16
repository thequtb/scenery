#!/bin/bash

case "$1" in
  "build")
    buildah from --name tg-bld docker.io/library/python:3.13-slim
    buildah copy tg-bld src /app
    buildah config --workingdir /app tg-bld

    buildah run tg-bld pip install --upgrade pip
    buildah run tg-bld pip install -r requirements.txt
    buildah config --cmd '["python", "-m", "bot"]' tg-bld
    buildah commit tg-bld tg-bld:latest
    ;;
    
  "update")
    buildah copy tg-bld src /app
    buildah run tg-bld pip install -r requirements.txt
    buildah commit tg-bld tg-bld:latest
    ;;
    
  "run")
    podman run --name tg --replace -d tg-bld:latest
    ;;
    
  *)
    echo "Usage: $0 {build|update|run}"
    exit 1
    ;;
esac

