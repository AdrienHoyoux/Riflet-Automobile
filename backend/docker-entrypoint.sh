#!/bin/sh
set -e

echo "Waiting for database..."
until python -c "
import os, MySQLdb
MySQLdb.connect(
    host=os.environ.get('DATABASE_HOST', 'db'),
    port=int(os.environ.get('DATABASE_PORT', '3306')),
    user=os.environ['MYSQL_USER'],
    passwd=os.environ['MYSQL_PASSWORD'],
    db=os.environ['MYSQL_DATABASE'],
)
" 2>/dev/null; do
  sleep 2
done

echo "Running migrations..."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
