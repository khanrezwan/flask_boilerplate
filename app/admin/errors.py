from flask import render_template
from . import admin_panel


@admin_panel.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@admin_panel.app_errorhandler(404)
def internal_server_error(e):
    return render_template('500.html'), 500


@admin_panel.app_errorhandler(404)
def internal_server_error(e):
    return render_template('403.html'), 403
