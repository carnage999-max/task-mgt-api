#!/bin/bash
# start.sh

# Start Gunicorn in background
gunicorn task_mgt.wsgi:application --bind 0.0.0.0:$PORT &

# Start Celery
celery -A task_mgt worker --loglevel=info
