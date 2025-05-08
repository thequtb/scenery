# Telegram Webhook System Deployment

This directory contains buildah scripts to deploy the Telegram webhook system.

## Components

1. **Redis** - Message streaming service
2. **PostgreSQL** - Database for message storage
3. **Spark** - Elixir Plug application that receives Telegram webhooks and forwards to Redis
4. **Journal** - Phoenix API that processes the streams and notifies users

## Prerequisites

- Buildah and Podman installed
- Elixir 1.15+ installed (for development)
- Telegram Bot Token

## Configuration

Before running the scripts, update these configurations:

1. In `journal.sh`, replace `YOUR_TELEGRAM_BOT_TOKEN` with your actual Telegram bot token:
   ```bash
   buildah config --env TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN" journal-release
   ```

2. Ensure you have network connectivity between containers.

## Deployment

You can deploy the entire system with a single command:

```bash
cd /home/qutb/scnr/buildah
chmod +x *.sh
./run-all.sh
```

Or deploy services individually:

```bash
# Deploy Redis
./redis.sh

# Deploy PostgreSQL
./psql.sh

# Deploy Spark (Telegram webhook service)
./spark.sh

# Deploy Journal (Phoenix API)
./journal.sh
```

## Post-Deployment

1. Configure your Telegram bot to use the webhook:
   ```
   https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=http://your-server:8080/webhook/telegram
   ```

2. Test the system by sending a message to your Telegram bot. The message should be processed and you should receive a notification with the message ID.

## Monitoring

You can check the logs for each service:

```bash
podman logs -f spark
podman logs -f journal
podman logs -f snr-rds-pg
podman logs -f snr-psql-pg
``` 