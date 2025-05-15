buildah from --name rds-bld docker.io/library/redis:8
buildah commit rds-bld rds-bld:latest
podman network create plugnet
podman run -d --network plugnet --name rds-bld rds-bld:latest