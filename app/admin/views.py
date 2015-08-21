__author__ = 'rezwan'
# Library imports
from flask_admin import BaseView, expose
from flask.ext.login import current_user
from flask import redirect, url_for, request, abort
from flask_admin.contrib.sqla import ModelView

# app related imports
from .. import admin
from ..models import User, Role
from app import db


class MyView(BaseView):
    @expose('/')
    def index(self):
        # if not login.current_user.is_authenticated():
        #     return redirect(url_for('.login_view'))
        # return super(MyAdminIndexView, self).ind

        return self.render('admin/index.html')

    def is_accessible(self):
        # print current_user.is_authenticated()
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        # print 'outside'
        if not self.is_accessible():
            print 'inside'
            abort(403)


class UserView(ModelView):
    # Override displayed fields
    column_list = ('username', 'email', 'role')

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(UserView, self).__init__(User, session, **kwargs)

    def is_accessible(self):
        # print current_user.is_admin()
        # print current_user.is_authenticated()
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        # print 'outside'
        if not self.is_accessible():
            abort(403)


class RoleView(ModelView):
    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(RoleView, self).__init__(Role, session, **kwargs)

    def is_accessible(self):
        # print current_user.is_admin()
        # print current_user.is_authenticated()
        return current_user.is_admin()

    def _handle_view(self, name, **kwargs):
        # print 'outside'
        if not self.is_accessible():
            abort(403)



admin.add_view(UserView(db.session))
admin.add_view(RoleView(db.session))


# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Logger, db.session))
# admin.add_view(ModelView(File, db.session))
# admin.add_view(ModelView(Sensor, db.session))
# admin.add_view(ModelView(Site, db.session))
# admin.add_view(ModelView(RawData, db.session))
# admin.add_view(ModelView(Role, db.session))
