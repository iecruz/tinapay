from peewee import *
from playhouse.shortcuts import model_to_dict
import datetime

db = PostgresqlDatabase(
    'yapanit',
    user='postgres',
    password='postgres',
    host='localhost'
)

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
    quanity=IntegerField(default=0)

class Order(BaseModel):
    user=ForeignKeyField(User)
    total=DecimalField(decimal_places=2)
    date=DateTimeField(default=datetime.date.today())
    time=TimeField(default=datetime.datetime.now().time())

class OrderList(BaseModel):
    order=ForeignKeyField(Order)
    bread=ForeignKeyField(Bread)
    quantity=IntegerField()

def initialize():
    db.connect()
    # db.drop_tables([Order, OrderList], safe=True)
    db.create_tables([User, Bread, Order, OrderList], safe=True)

def drop(table):
    db.drop_table(table, fail_silently=True)

def close():
    db.close()
