#!/bin/bash
# Journal - Phoenix API microservice buildah script

# Build container
buildah from --name journal-build docker.io/elixir:1.15-alpine
buildah run journal-build apk add --no-cache build-base git

# Set working directory
buildah config --workingdir /app journal-build

# Copy mix files
buildah copy journal-build /home/qutb/scnr/journal/mix.exs /app/
buildah copy journal-build /home/qutb/scnr/journal/mix.lock /app/ 2>/dev/null || true

# Get and compile dependencies
buildah run journal-build mix local.hex --force
buildah run journal-build mix local.rebar --force
buildah run journal-build mix deps.get
buildah run journal-build mix deps.compile

# Copy app code
buildah copy journal-build /home/qutb/scnr/journal/lib /app/lib
buildah copy journal-build /home/qutb/scnr/journal/priv /app/priv
buildah copy journal-build /home/qutb/scnr/journal/config /app/config

# Compile application
buildah run journal-build MIX_ENV=prod mix compile

# Run migrations
buildah run journal-build MIX_ENV=prod mix ecto.create
buildah run journal-build MIX_ENV=prod mix ecto.migrate

# Build release
buildah run journal-build MIX_ENV=prod mix release

# Create release image
buildah from --name journal-release docker.io/alpine:3.19
buildah run journal-release apk add --no-cache libstdc++ ncurses-libs postgresql-client

# Copy release from build container
buildah config --workingdir /app journal-release
buildah copy --from=journal-build journal-release /app/_build/prod/rel/journal /app/

# Set environment variables
buildah config --env LANG=C.UTF-8 journal-release
buildah config --env MIX_ENV=prod journal-release
buildah config --env PORT=4000 journal-release
buildah config --env REDIS_HOST=snr-rds-pg journal-release
buildah config --env REDIS_PORT=6379 journal-release
buildah config --env DATABASE_URL="ecto://postgres:postgres@snr-psql-pg/journal_prod" journal-release
buildah config --env SECRET_KEY_BASE="fnpY3vDUvy5VhxhXC5VT3i/BupEr0v3/kK5vA4IxtDm1LrTYqX8Qye4V1DpgF4Dl" journal-release
buildah config --env TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN" journal-release

# Expose port
buildah config --port 4000 journal-release

# Set default command
buildah config --cmd '["/app/bin/journal", "start"]' journal-release

# Commit image
buildah commit journal-release journal:latest

# Clean up
buildah rm journal-build
buildah rm journal-release

# Run container
podman run -d --network plugnet --name journal -p 4000:4000 journal:latest 