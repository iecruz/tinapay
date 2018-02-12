from flask import Blueprint, render_template, request, redirect, url_for
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

    return render_template('admin/order.html', order_list=order_list, order=order)

@app.route('/order/list/')
def order_list():
    try:
        bread=[model_to_dict(bread) for bread in Bread.select()]
        total=float(0)

        for i, item in enumerate(bread):
            bread[i]['order']=model_to_dict(OrderList.select(fn.Sum(OrderList.quantity).alias('quantity')).join(Bread, on=(OrderList.bread==Bread.id)).where(Bread.id==item['id']).first())['quantity']
            bread[i]['amount']="{0:.2f}".format(float(item['order'] * item['price']))
            total=total+float(item['order'] * item['price'])

    except DoesNotExist:
        bread=None

    return render_template('admin/list.html', bread=bread, total="{0:.2f}".format(total))
