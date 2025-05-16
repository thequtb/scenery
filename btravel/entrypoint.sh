#!/bin/bash
set -euo pipefail

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run Django migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Running gunicorn
echo "Starting Gunicorn..."
exec gunicorn adm.wsgi:application --bind 0.0.0.0:8000 --workers 4


