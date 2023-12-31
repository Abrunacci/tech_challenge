#! /bin/bash
set -e

while [[ "$(curl -s -o /dev/null --insecure -w ''%{http_code}'' ${ELASTICSEARCH_HOST}:${ELASTICSEARCH_PORT})" != "200" ]]; do
  echo 'Waiting for elasticsearch'
  sleep 5;
done

echo 'Starting app...'
uvicorn src.main:app --reload --host 0.0.0.0 --log-level debug