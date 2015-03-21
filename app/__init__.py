import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID

from config import basedir

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