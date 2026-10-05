#!/bin/sh
set -eu

if [ -z "${DATABASE_URL:-}" ]; then
  : "${DB_USER:?Falta DB_USER}"
  : "${DB_PASSWORD:?Falta DB_PASSWORD}"
  : "${DB_HOST:?Falta DB_HOST}"
  : "${DB_PORT:?Falta DB_PORT}"
  : "${DB_NAME:?Falta DB_NAME}"
  export DATABASE_URL="postgresql+asyncpg://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
fi

python /app/entrypoint.py
python -m app.db.init_db

if [ "$#" -eq 0 ]; then
  set -- uvicorn app.main:app --host 0.0.0.0 --port 8000
fi

exec "$@"
