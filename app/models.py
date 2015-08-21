import re
import datetime
from app import db
from sqlalchemy.engine import Engine
from sqlalchemy import event

############# Uncomment if using Sqlite##########################################################
# @event.listens_for(Engine, "connect")
# def set_sqlite_pragma(dbapi_connection, connection_record):
#     """
#      A function that listens to sqlite connection and turns on paragma foreign_key parameter to enforce cascade delete
#      and updates. passive delete will not work without this helper
#     :param dbapi_connection:
#     :param connection_record:
#     :return:
#     """
#
#     cursor = dbapi_connection.cursor()
#     cursor.execute("PRAGMA foreign_keys=ON")
#     cursor.close()
###################################################################################################

#######################################################################################################################
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'auth_user'
    id = db.Column(db.Integer, primary_key=True)

    # User Name
    username = db.Column(db.String(128), nullable=False, unique=True, index=True)
    # Identification Data: email & password
    email = db.Column(db.String(128), nullable=False,index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    # Authorisation Data: role & status

    status = db.Column(db.SmallInteger, nullable=True)
    # New instance instantiation procedure
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        query = Role.query.filter(Role.id == self.role_id).one()
        if query.name == 'admin':
            return True
        else:
            return False

    def get_current_user_role(self):
        query = Role.query.filter(Role.id == self.role_id).one()
        return str(query.name).lower()

##########################################################################
from flask.ext.login import AnonymousUserMixin


class AnonymousUser(AnonymousUserMixin):
    '''
        Added this to protect flask-admin blueprint
    '''
    def is_admin(self):
        return False

login_manager.anonymous_user = AnonymousUser


#############################################################################################################3333
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return 'Role <%r>' % self.name
###################################################
