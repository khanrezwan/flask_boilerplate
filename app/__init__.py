# Library imports
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
# from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config
from flask.ext.admin import Admin
from datetime import timedelta
# from flask_admin import Admin

#App Sepcific imports
# from models import User, Role

bootstrap = Bootstrap()
# mail = Mail()
moment = Moment()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

admin = Admin(name='Wind Data Viewer Admin')
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    # mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    # Todo-rezwan follow this guide for auto renewing session
    # http://stackoverflow.com/questions/19760486/resetting-the-expiration-time-for-a-cookie-in-flask
    # http://stackoverflow.com/questions/19760486/resetting-the-expiration-time-for-a-cookie-in-flask
    app.permanent_session_lifetime = timedelta(minutes=60)  # adding session time out. working

    # attach routes and custom error pages here
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .admin import admin_panel as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    db.app = app
    db.create_all()


    return app
