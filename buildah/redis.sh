buildah from --name snr-rds-pg docker.io/library/redis:8
buildah commit snr-rds-pg snr-rds-pg:latest
podman network create plugnet
podman run -d --network plugnet --name snr-rds-pg snr-rds-pg:latest