from flask import Blueprint, render_template, request, redirect, url_for, session
from peewee import DoesNotExist, fn
from playhouse.shortcuts import model_to_dict
from core.models import Bread, Order, OrderList
from core.forms import AddBreadForm
import datetime

app = Blueprint('admin', __name__)

@app.route('/inventory/', methods=['GET', 'POST'])
def inventory():
    form=AddBreadForm(request.form)
    if request.method == 'POST' and form.validate():
        Bread.create(
            name=form.name.data.title(),
            price=round(form.price.data, 2)
        )
        return redirect(url_for('admin.inventory'))
    try:
        bread=Bread.select()
    except DoesNotExist:
        bread=None
        
    return render_template('admin/inventory.html', form=form, bread=bread)

@app.route('/order/card/')
def order_card():
    try:
        order_list=[model_to_dict(order_list) for order_list in OrderList.select().join(Order)]
        order=[model_to_dict(order) for order in Order.select().where(Order.date==datetime.date.today())]
    except DoesNotExist:
        order=None
        order_list=None

    return render_template('admin/card.html', order_list=order_list, order=order)

@app.route('/order/list/')
def order_list():
    try:
        bread=[]
        total=float(0)

        for item in [model_to_dict(bread) for bread in Bread.select()]:
            quantity=model_to_dict(
                OrderList.select(fn.Sum(OrderList.quantity).alias('quantity'))
                .join(Order, on=(OrderList.order==Order.id))
                .join(Bread, on=(OrderList.bread==Bread.id))
                .where(Order.date==datetime.date.today(), Bread.id==item['id'])
                .get())['quantity']

            if quantity is None:
                continue

            item['order']=quantity
            item['amount']="{0:.2f}".format(float(quantity * item['price']))

            bread.append(item)
            total=total+float(quantity * item['price'])

    except DoesNotExist:
        bread=None

    return render_template('admin/list.html', bread=bread, total="{0:.2f}".format(total))
