from flask import Blueprint, render_template, request, redirect, url_for
from core.models import Bread, Order, OrderList
from core.forms import AddBreadForm
from playhouse.shortcuts import model_to_dict
import datetime

app = Blueprint('admin', __name__)

@app.route('/inventory/', methods=['GET', 'POST'])
def inventory():
    form=AddBreadForm(request.form)
    if request.method == 'POST' and form.validate():
        Bread.create(
            name=form.name.data,
            price=round(form.price.data, 2)
        )
        return redirect(url_for('admin.inventory'))
    try:
        bread=Bread.select()
    except DoesNotExist:
        bread=None
        
    return render_template('admin/inventory.html', form=form, bread=bread)

@app.route('/order/')
def order():
    try:
        order_list=[model_to_dict(order_list) for order_list in OrderList.select().join(Order)]
        order=[model_to_dict(order) for order in Order.select().where(Order.date==datetime.date.today())]
    except DoesNotExist:
        order_list=None

    return render_template('admin/order.html', order_list=order_list, order=order)
