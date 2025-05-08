#!/bin/bash
# Build container
buildah from --name sprk-plg-pg docker.io/elixir:1.18

# Set working directory
buildah config --workingdir /app sprk-plg-pg

# Copy application code
buildah copy sprk-plg-pg . /app/

# Get and compile dependencies
buildah run sprk-plg-pg mix local.hex --force
buildah run sprk-plg-pg mix local.rebar --force
buildah run sprk-plg-pg mix deps.get
buildah run sprk-plg-pg mix deps.compile

# Set environment variables
buildah config --env WEBHOOK_PORT=8000 sprk-plg-pg
buildah config --env REDIS_HOST=snr-rds-pg sprk-plg-pg
buildah config --env REDIS_PORT=6379 sprk-plg-pg

# Expose port
buildah config --port 8000 sprk-plg-pg

# Set command to run the application without halting
buildah config --cmd '["mix", "run", "--no-halt"]' sprk-plg-pg

# Commit the container to an image
buildah commit sprk-plg-pg spark:latest