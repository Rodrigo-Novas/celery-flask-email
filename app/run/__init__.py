import os
from flask import Flask
from celery import Celery
from flask_mail import Mail
from views import email

URLS = (("/email", email))


def create_app():
    app =  Flask(__name__)
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = 'novasr4516@gmail.com'
    celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)
    mail = Mail(app)
    app.config['MAIL'] = mail
    app.config['CELERY'] = celery
    app.url_map.strict_slashes = False

    for url, blueprint in URLS:
        app.register_blueprint(blueprint, url_prefix=url)

    return app
