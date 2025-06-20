#!/bin/bash
# start.sh

# Start Gunicorn in background
gunicorn task_mgt.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 1 --timeout 60 &

# Start Celery
celery -A task_mgt worker --pool=solo --loglevel=info
