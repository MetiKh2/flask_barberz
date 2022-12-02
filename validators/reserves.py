from flask_wtf import FlaskForm 
from wtforms.fields import StringField , DateField , SubmitField,SelectMultipleField
from wtforms.validators import DataRequired , Length , Email , EqualTo

class CreateReserveForm(FlaskForm):

    fullname = StringField(name='fullname' , 
    validators=[DataRequired('fullname Field is Required')])

    phone = StringField(name='phone' , 
    validators=[DataRequired('phone Field Is Required') ])
    
    description = StringField(name='description')
    
    date = DateField(name='date' , 
    validators=[DataRequired('date Field Is Required') ])
    
    time = StringField(name='time' , 
    validators=[DataRequired('time Field Is Required') ])
    
    services = SelectMultipleField(coerce=int,name='services',validators=[DataRequired()])
    
    submit = SubmitField('Create Reserve')

class EditServiceForm(FlaskForm):
    title = StringField(name='title' , 
    validators=[DataRequired('Title Field is Required')])

    price = StringField(name='price' , 
    validators=[DataRequired('Price Field Is Required') ])

    submit = SubmitField('Edit Reserve')