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
COPY flaskblog.py config.py docker/flaskblog/start.sh ./

# run-time configuration
EXPOSE 5000
ENTRYPOINT ["./start.sh"]
