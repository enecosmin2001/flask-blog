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
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKBLOG_SLOW_DB_QUERY_TIME = 0.5
    SSL_REDIRECT = False

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
    SERVER_NAME = "127.0.0.1:8943"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "TEST_DATABASE_URL"
    ) or "sqlite:////" + os.path.join(basedir, "data-test.sqlite")


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "data.sqlite")

    SSL_REDIRECT = True
    DEBUG = False

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler

        credentials = None
        secure = None

        if getattr(cls, "MAIL_USERNAME", None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, "MAIL_USE_TLS", None):
                secure = ()

        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FLASKBLOG_MAIL_SENDER,
            toaddrs=[cls.FLASKBLOG_ADMIN],
            subject=cls.FLASKBLOG_MAIL_SUBJECT_PREFIX + " Application Error",
            credentials=credentials,
            secure=secure,
        )

        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get("DYNO") else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "heroku": HerokuConfig,
    "default": DevelopmentConfig,
}
