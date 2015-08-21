from flask import Blueprint
admin_panel = Blueprint('admin_app', __name__)
from . import views, errors
