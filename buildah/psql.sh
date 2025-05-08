buildah from --name snr-psql-pg postgres:17.4
buildah run snr-psql-pg apt install -y postgresql-common
buildah run snr-psql-pg apt install -y postgresql-17-pgvector
buildah copy snr-psql-pg pg-init/init.sql /docker-entrypoint-initdb.d/init.sql