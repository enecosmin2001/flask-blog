import os

from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard to guess string"
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    FLASKBLOG_MAIL_SUBJECT_PREFIX = os.environ.get("FLASKBLOG_MAIL_SUBJECT_PREFIX")
    FLASKBLOG_MAIL_SENDER = os.environ.get("FLASKBLOG_MAIL_SENDER")
    FLASKBLOG_ADMIN = os.environ.get("FLASKBLOG_ADMIN")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKBLOG_POSTS_PER_PAGE = int(os.environ.get("FLASKBLOG_POSTS_PER_PAGE"))
    FLASKBLOG_FOLLOWERS_PER_PAGE = int(os.environ.get("FLASKBLOG_FOLLOWERS_PER_PAGE"))
    FLASKBLOG_COMMENTS_PER_PAGE = int(os.environ.get("FLASKBLOG_FOLLOWERS_PER_PAGE"))

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DEV_DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data-dev.sqlite")


class TestingConfig(Config):
    TESTING = True
    # PRESERVE_CONTEXT_ON_EXCEPTION = False
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "127.0.0.1"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL"
    ) or "sqlite:////" + os.path.join(basedir, "data-test.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
