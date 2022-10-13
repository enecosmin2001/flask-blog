#!/bin/sh
source venv/bin/activate

celery -A app.celery_worker:celery worker --loglevel=info
