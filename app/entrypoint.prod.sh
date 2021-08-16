#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 5
      echo "Waiting for postgres..."
    done

    echo "PostgreSQL started"
fi

gunicorn config.wsgi:application --bind 0.0.0.0:8000 --certfile=/etc/certs/$SSL_CERTIFICATE --keyfile=/etc/certs/$SSL_CERTIFICATE_KEY

exec "$@"