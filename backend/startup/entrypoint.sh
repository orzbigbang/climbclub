#!/bin/bash
#set -e
uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8080 --loop uvloop --reload
#if [ "$BUILD_ENV" = "prod" ]; then
#    echo "Running in workers mode"
#    gunicorn -c "$GUNICORN_CONF" main:app
#else:
#    echo "Running in reload mode"
#    uvicorn main:app --proxy-headers --host 0.0.0.0 --port 8080 --loop uvloop --reload
#fi
