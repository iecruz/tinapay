from flask import Blueprint, render_template, request, redirect, url_for, session
from peewee import *
from core.models import Bread, Order, OrderList, User
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
        item=[order_list for order_list in OrderList
            .select(OrderList, Bread.name.alias('bread_name'))
            .join(Bread)
            .dicts()]
        order=[order for order in Order
            .select(Order, fn.Concat(User.first_name, ' ', User.last_name).alias('user_name'))
            .join(User)
            .where(Order.date==datetime.date.today())
            .dicts()]
    except DoesNotExist:
        order=None
        item=None

    return render_template('admin/card.html', item=item, order=order)

@app.route('/order/list/')
def order_list():
    total=0

    try:
        bread=[row for row in Bread
            .select(Bread.name, Bread.price, fn.Sum(OrderList.quantity).alias('count'))
            .join(OrderList, JOIN.LEFT_OUTER)
            .join(Order)
            .where(Order.date==datetime.date.today())
            .group_by(Bread)
            .order_by(Bread.name)
            .dicts()]

    except DoesNotExist:
        bread=None

    total=float(sum([row['price'] * row['count'] for row in bread]))

    return render_template('admin/list.html', bread=bread, total="{0:.2f}".format(total))
