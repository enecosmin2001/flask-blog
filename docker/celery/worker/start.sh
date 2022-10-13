#!/bin/sh
source venv/bin/activate

celery -A celery_worker.celery worker --loglevel=info
