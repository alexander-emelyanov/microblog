import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD, MAIL_SECURE

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import models

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))


@lm.user_loader
def load_user(id):
    return models.User.query.get(int(id))

from app import views


# Error handling
if not app.debug:

    import logging
    from logging.handlers import SMTPHandler

    credentials = None
    secure = None

    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)

    if MAIL_SECURE:
        secure = MAIL_SECURE

    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), MAIL_USERNAME, ADMINS, 'Microblog failure', credentials, secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)