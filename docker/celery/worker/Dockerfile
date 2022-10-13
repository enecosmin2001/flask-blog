FROM python:3.9-alpine

RUN adduser -D celeryworker
USER celeryworker

WORKDIR /home/celeryworker

COPY requirements/celery.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app/celery_worker.py ./

COPY docker/celery/worker/start.sh ./

USER root
RUN chmod +x start.sh

USER celeryworker

# run-time configuration
ENTRYPOINT ["./start.sh"]
