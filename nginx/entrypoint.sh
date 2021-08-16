#!/bin/sh
set -eu

envsubst '${SERVER_NAME} ${SSL_CERTIFICATE} ${SSL_CERTIFICATE_KEY}' < /etc/nginx/conf.d/mynginx.tmp > /etc/nginx/conf.d/mynginx.conf

exec "$@"