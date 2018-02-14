from wtforms import Form, StringField, DecimalField, IntegerField, PasswordField, SelectField
from wtforms.validators import *
from core import models
import peewee

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
    try:
        bread=SelectField('Bread', choices=[(row['id'], "{} (P {})".format(row['name'], row['price'])) for row in models.Bread.select().order_by(models.Bread.name).dicts()], coerce=int)
    except peewee.DoesNotExist:
        bread=SelectField('Bread', choices=[])
    except peewee.ProgrammingError:
        bread=SelectField('Bread', choices=[])
    quantity=IntegerField('Quantity', [NumberRange(min=0), InputRequired()])
