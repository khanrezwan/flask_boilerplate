from flask.ext.wtf import Form
from wtforms import SubmitField, PasswordField, StringField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, regexp


class UploadForm(Form):
    datafiles = StringField('Upload Files')
