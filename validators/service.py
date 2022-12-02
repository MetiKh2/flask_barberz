from flask_wtf import FlaskForm 
from wtforms.fields import StringField , PasswordField , SubmitField
from wtforms.validators import DataRequired , Length , Email , EqualTo

class CreateServiceForm(FlaskForm):
    title = StringField(name='title' , 
    validators=[DataRequired('Title Field is Required')])

    price = StringField(name='price' , 
    validators=[DataRequired('Price Field Is Required') ])

    submit = SubmitField('Create User')

class EditServiceForm(FlaskForm):
    title = StringField(name='title' , 
    validators=[DataRequired('Title Field is Required')])

    price = StringField(name='price' , 
    validators=[DataRequired('Price Field Is Required') ])

    submit = SubmitField('Create User')