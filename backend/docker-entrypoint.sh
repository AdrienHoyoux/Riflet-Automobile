#!/bin/sh
set -e

echo "Waiting for database..."
attempt=0
until python <<'PY'
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import connection

connection.ensure_connection()
PY
do
  attempt=$((attempt + 1))
  if [ "$attempt" -ge 30 ]; then
    echo "Database not ready after 60 seconds."
    exit 1
  fi
  echo "Database unavailable - retrying in 2s..."
  sleep 2
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Seeding initial data..."
python manage.py seed_data

echo "Starting application..."
exec "$@"
