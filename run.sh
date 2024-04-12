#!/bin/bash

IMAGE=rkashapov/solidsign-backend:latest

mkdir db
docker run \
  -p 80:8000 \
  -v db:/opt/app/db \
  -d \
  --env-file .env \
  $IMAGE \
  gunicorn -b 0.0.0.0:8000 backend.wsgi
