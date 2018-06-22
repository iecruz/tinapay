from flask import Flask
from peewee import *
from playhouse.db_url import connect
import datetime
import os

app=Flask(__name__)
app.config.from_object('core.config.ProductionConfig')

db=connect(os.getenv('DATABASE_URL'))

class BaseModel(Model):
    class Meta:
        database=db

class User(BaseModel):
    username=CharField(primary_key=True, unique=True)
    password=CharField()
    first_name=CharField()
    last_name=CharField()

class Bread(BaseModel):
    name=CharField()
    price=DecimalField(decimal_places=2)
    quantity=IntegerField(default=0)

class Order(BaseModel):
    user=ForeignKeyField(User)
    total=DecimalField(decimal_places=2)
    date=DateTimeField(default=datetime.date.today())
    time=TimeField(default=datetime.datetime.now().time())
    status=CharField(default='Order Placed')

class OrderList(BaseModel):
    order=ForeignKeyField(Order)
    bread=ForeignKeyField(Bread)
    quantity=IntegerField()
    
db_table=[User, Bread, Order, OrderList]

def initialize():
    db.connect(reuse_if_open=True)
    db.create_tables(db_table, safe=True)

def close():
    db.close()
