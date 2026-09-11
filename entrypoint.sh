#!/usr/bin/env bash
set -euo pipefail

# Stop early if required settings are missing.
required_variables=(
  SECRET_KEY
  DB_NAME
  DB_USER
  DB_PASSWORD
  DB_HOST
  DB_PORT
  DJANGO_SUPERUSER_USERNAME
  DJANGO_SUPERUSER_EMAIL
  DJANGO_SUPERUSER_PASSWORD
)

for variable_name in "${required_variables[@]}"; do
  # Read the value of each variable name from the list above.
  if [[ -z "${!variable_name:-}" ]]; then
    echo "Required environment variable ${variable_name} is missing or empty." >&2
    exit 1
  fi
done

echo "Waiting for PostgreSQL to accept connections ..."

# Wait five seconds before checking the database again.
while ! nc -z "${DB_HOST}" "${DB_PORT}"; do
  sleep 5
done

echo "PostgreSQL is reachable."

python manage.py migrate

python manage.py collectstatic --noinput

# Create the superuser only if it does not already exist.
python manage.py shell <<'PYTHON'
import os

from django.contrib.auth import get_user_model

user_model = get_user_model()
username = os.environ["DJANGO_SUPERUSER_USERNAME"]

if user_model.objects.filter(username=username).exists():
    print("Django superuser already exists; skipping creation.")
else:
    user_model.objects.create_superuser(
        username=username,
        email=os.environ["DJANGO_SUPERUSER_EMAIL"],
        password=os.environ["DJANGO_SUPERUSER_PASSWORD"],
    )
    print("Django superuser created.")
PYTHON

# Make Gunicorn the main process so Docker can stop it correctly.
exec gunicorn tsa_app.wsgi:application --bind 0.0.0.0:8000
