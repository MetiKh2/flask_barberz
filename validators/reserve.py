from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField,SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from db_manager import db
from models import Service
class ReserveForm(FlaskForm):
    fullname = StringField(name='fullname',
                                  validators=[DataRequired('نام را وارد کنید')])
    phone = StringField(name='phone',
                                  validators=[DataRequired('تلفن را وارد کنید')])
    description = TextAreaField(name='description')
    services = SelectMultipleField(coerce=int,name='services',validators=[DataRequired()])


    submit = SubmitField()

 