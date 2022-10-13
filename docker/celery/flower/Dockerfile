FROM python:3.9-alpine

RUN adduser -D celeryflower
USER celeryflower

WORKDIR /home/celeryflower

COPY requirements/celery.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app/celery_worker.py ./

COPY docker/celery/flower/start.sh ./

USER root
RUN chmod +x start.sh

USER celeryflower

# run-time configuration
EXPOSE 5555
ENTRYPOINT ["./start.sh"]
