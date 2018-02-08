from wtforms import Form, StringField, DecimalField, IntegerField, PasswordField, SelectField
from wtforms.validators import *
from playhouse.shortcuts import model_to_dict
from core import models

class RegistrationForm(Form):
    first_name=StringField('First Name', [Length(max=32), InputRequired()])
    last_name=StringField('Last Name', [Length(max=32), InputRequired()])
    username=StringField('Username', [Length(min=4, max=20), InputRequired()])
    password=PasswordField('Password', [Length(min=8, max=32), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password=PasswordField('Confirm Password', [Length(min=8, max=32)])

class LoginForm(Form):
    username=StringField('Username', [Length(min=4, max=20), InputRequired()])
    password=PasswordField('Password', [Length(min=8, max=32), InputRequired()])

class AddBreadForm(Form):
    name=StringField('Name', [Length(max=32), InputRequired()])
    price=DecimalField('Price', [NumberRange(min=0), InputRequired()], places=2)

class AddOrderForm(Form):
    bread=SelectField('Bread', choices=[(bread['id'], bread['name']) for bread in (model_to_dict(bread) for bread in models.Bread.select())], coerce=int)
    quantity=IntegerField('Quantity', [NumberRange(min=0), InputRequired()])