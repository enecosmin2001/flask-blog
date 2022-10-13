FROM python:3.9-alpine

ENV FLASK_APP flaskblog.py
ENV FLASK_CONFIG docker

RUN adduser -D flaskblog
USER flaskblog

WORKDIR /home/flaskblog

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY flaskblog.py config.py ./

COPY ./scripts/flaskblog/start.sh ./start_flaskblog.sh
COPY ./scripts/celery/worker/start.sh ./start_celery_worker.sh
COPY ./scripts/celery/flower/start.sh ./start_celery_flower.sh

USER root
RUN chmod +x ./start_flaskblog.sh
RUN chmod +x ./start_celery_worker.sh
RUN chmod +x ./start_celery_flower.sh

USER flaskblog

# run-time configuration
EXPOSE 5000
