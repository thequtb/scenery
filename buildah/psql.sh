buildah from --name pg-bld docker.io/postgres:17.4
buildah run pg-bld bash -c "apt update && apt upgrade -y && apt install -y postgresql-17-pgvector"
buildah copy pg-bld pg-init/init.sql /docker-entrypoint-initdb.d/init.sql
buildah commit pg-bld pg:latest