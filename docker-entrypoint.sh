#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput



# Wait for postgress initialization
wait-for-it db:5432 -t 120

# Make migrations
# python manage.py makemigrations

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
gunicorn storecard.wsgi:application --bind 0.0.0.0:$PORT