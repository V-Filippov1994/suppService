#!/bin/bash

postgres_ready() {
python << END
import sys
import psycopg2

try:
    psycopg2.connect("postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_HOST}:${POSTGRES_PORT}/postgres")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

alembic upgrade head

uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
