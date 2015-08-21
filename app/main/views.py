# Library Imports
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, flash, g
from flask.ext.login import login_required, current_user
# from werkzeug import check_password_hash, generate_password_hash
from flask import current_app as app
from werkzeug import secure_filename
import os
# App specific imports

from . import main
from .forms import *


from .. import db


from ..decorators import base_page_dictionary_builder, requires_roles


def build_logged_in_gist_view():

    return {
        'Some_key': 'some_value',

        }
    pass


@main.route('/', methods=['GET', 'POST'])
def index():
    if current_user.is_authenticated() == True:
        param_dict = build_logged_in_gist_view()
        return render_template('index.html', **param_dict)
    else:
        return render_template('index.html')
    pass


