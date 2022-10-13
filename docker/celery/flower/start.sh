#!/bin/sh
source venv/bin/activate

celery -A celery_worker.celery flower --loglevel=info
