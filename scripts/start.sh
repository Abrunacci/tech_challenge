#! /bin/bash
set -e

while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' elasticsearch:9200)" != "200" ]]; do
  echo 'Waiting for elasticsearch'
  sleep 5;
done

echo 'Starting app...'
uvicorn src.main:app --reload --host 0.0.0.0