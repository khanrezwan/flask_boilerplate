__author__ = 'rezwan'
from functools import wraps
from flask.ext.login import current_user
from flask import abort, flash

def base_page_dictionary_builder(brand_name='', navbar_dynamic_lis=list(),
                                 navbar_view_specific_left_col_buttons=list()):
    """
    This function creates dictionary data structure for the base template page.
    :param brand_name: Navigation bar brand name
    :param navbar_dynamic_lis: Top navbar dynamic button elements. it's a python list of lists.
    e.g.: [['Name of button 1', 'url'], ['Name of button 2', 'url'], ['Name of button 1']]
    :param navbar_view_specific_left_col_buttons: Left navigation panel buttons.it's a python list of lists.
    e.g.: [['Name of button 1', 'url'], ['Name of button 2', 'url'], ['Name of button 1']]
    :return: a dictionary of base page parameters, to be unpacked by flask built-in render_template function
    """
    return {'brand_name': brand_name, 'navbar_dynamic_lis': navbar_dynamic_lis,
            'navbar_view_specific_left_col_buttons': navbar_view_specific_left_col_buttons}


def requires_roles(*roles):
    """
    http://flask.pocoo.org/snippets/98/
    @required_roles('admin', 'user')
    :param roles: string(s) of role name(s)
    :return:
    """
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.get_current_user_role() not in roles:
                flash('You don\'t have permission to perform this action')
                abort(403)
            return f(*args, **kwargs)
        return wrapped
    return wrapper
