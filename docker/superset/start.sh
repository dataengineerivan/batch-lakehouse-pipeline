#!/bin/bash
set -e
# First-time setup is safe to repeat on every start
superset db upgrade
superset fab create-admin --username "$SUPERSET_ADMIN_USER" --password "$SUPERSET_ADMIN_PASSWORD" \
  --firstname Admin --lastname User --email admin@example.com || true
superset init
exec gunicorn --bind 0.0.0.0:8088 --workers 2 --timeout 120 "superset.app:create_app()"
