from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField #MultipleCheckboxField() instead of SelectMultipleField() ,SelectMultipleField , SelectField
from wtforms.validators import DataRequired
from utils.forms import MultipleCheckboxField

class Postform(FlaskForm):
    title = TextField(validators=[DataRequired()])
    summary = TextAreaField()
    content = TextAreaField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    categories = MultipleCheckboxField(coerce=int) # i create  in utils forms / instead of SelectMultipleField() | coerce= is necessary
    
    
class Categoryform(FlaskForm):
    name = TextField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    description = TextAreaField()
