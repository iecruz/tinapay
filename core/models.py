from flask import current_app
from peewee import *
from playhouse.shortcuts import model_to_dict
import datetime

db_config={
    'database':'d7mq3n8b6u3sfc', 
    'user':'xnmnsceybattno', 
    'password':'f9f5203832a95dddcdac98aff4e83ca33a7b4778f5b87ae89f72364ea08d0da4', 
    'host':'ec2-54-217-236-201.eu-west-1.compute.amazonaws.com'
}
# db_config={'database': 'yapanit', 'user':'postgres', 'password':'postgres', 'host':'localhost'}
db = PostgresqlDatabase(db_config['database'], user=db_config['user'], password=db_config['password'], host=db_config['host'])

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
    
db_table=[User, Bread, Order, OrderList]

def config(db, **kwargs):
    db_config['database']=db
    if kwargs:
        for key, val in kwargs.items():
            db_config['key']=val
    db = PostgresqlDatabase(db_config['database'], user=db_config['user'], password=db_config['password'], host=db_config['host'])

def initialize():
    db.connect()
    db.create_tables(db_table, safe=True)

def close():
    db.close()
