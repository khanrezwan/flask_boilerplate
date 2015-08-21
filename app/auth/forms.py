from flask.ext.wtf import Form
from wtforms import SubmitField, PasswordField, StringField, BooleanField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, EqualTo, Regexp, Length
from ..models import User, Role



class LoginForm(Form):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberme = BooleanField('Remember Me', default=False)
    submit = SubmitField('Submit')


class RegisterUser(Form):

    username = StringField('User Name', validators=[DataRequired(),Length(1, 64),
                                                    Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                                                           0, 'Usernames must have only letters, '
                                                              'numbers, dots or underscores')])
    email = StringField('E-Mail', validators=[Email(), DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', 'Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[DataRequired()])
    role = QuerySelectField(label='Role', get_label='name')
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class AddRoles(Form):
    name = StringField('Role', validators=[DataRequired()])
    submit = SubmitField('Add')

    def validate_name(self, field):
        if Role.query.filter_by(name=field.name.lower()).first():
            raise ValidationError('Role already registered.')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired(),
                                                         EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')
