FROM elixir:1.15-alpine AS build

# Install build dependencies
RUN apk add --no-cache build-base

WORKDIR /app

# Copy mix dependencies files
COPY mix.exs mix.lock ./

# Get and compile dependencies
RUN mix local.hex --force && \
    mix local.rebar --force && \
    mix deps.get && \
    mix deps.compile

# Copy application code
COPY . .

# Compile the application
RUN mix compile

# Build release
RUN mix release

# Start a new stage for the minimal runtime image
FROM alpine:3.19

RUN apk add --no-cache libstdc++ ncurses-libs postgresql-client

WORKDIR /app

# Copy the release from the build stage
COPY --from=build /app/_build/dev/rel/journal ./

# Set environment variables
ENV LANG=C.UTF-8 \
    MIX_ENV=prod \
    PORT=4000 \
    REDIS_HOST=localhost \
    REDIS_PORT=6379 \
    DATABASE_URL="ecto://postgres:postgres@localhost/journal_prod" \
    SECRET_KEY_BASE="CHANGE_ME_IN_PRODUCTION"

EXPOSE 4000

CMD ["/app/bin/journal", "start"] 