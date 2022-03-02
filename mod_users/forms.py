from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms import PasswordField , StringField
from wtforms.validators import DataRequired


class Loginform(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])

class Registerform(FlaskForm):
    full_name = StringField()
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired()])