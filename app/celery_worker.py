import os
import time

from celery import Celery
from dotenv import load_dotenv

load_dotenv("../env-docker")

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND_URL")

from app import create_app, db
from app.services.dreamer import Dreamer


@celery.task(name="generate_dream_image")
def generate_dream_image(post_id, text_to_image):
    app = create_app("docker")
    app_context = app.app_context()
    app_context.push()

    image_path = Dreamer.generate_dream_image(post_id, text_to_image)

    app_context.pop()
    db.session.remove()

    del app
    return image_path
