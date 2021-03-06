from flask import Blueprint, render_template, request, redirect, url_for, session
from peewee import DoesNotExist
from core.models import Bread, User, Order, OrderList, db
from core.forms import AddOrderForm

app = Blueprint('shop', __name__)

@app.route('/shop/', methods=['GET', 'POST'])
def shop():
    form=AddOrderForm(request.form)
    total=0

    if 'username' not in session:
        return redirect(url_for('user.login'))

    if 'basket' not in session:
        session['basket']={}

    basket=session['basket']
    
    if request.method == 'POST' and form.validate():
        basket[str(form.bread.data)]=int(form.quantity.data)
        session['basket']=basket

    try:
        bread={str(bread['id']): {'name': bread['name'], 'price': bread['price']} for bread in Bread.select().order_by(Bread.name).dicts()}
    except DoesNotExist:
        bread=None

    total=float(sum([bread.get(bread_id, None).get('price', None) * qty for bread_id, qty in basket.items()]))

    return render_template('shop.html', bread=bread, form=form, total="{0:.2f}".format(total))

@app.route('/shop/empty/')
def empty_basket():
    session.pop('basket', None)
    return redirect(url_for('shop.shop'))

@app.route('/order/')
def place_order():
    if 'basket' not in session:
        return redirect(url_for('shop.shop'))

    basket=session['basket']
    total=float(0)

    try:
        bread={str(bread['id']): {'name': bread['name'], 'price': bread['price']} for bread in Bread.select().order_by(Bread.name).dicts()}
    except DoesNotExist:
        bread=None
    
    total=float(sum([bread.get(bread_id, None).get('price', None) * qty for bread_id, qty in basket.items()]))

    order=Order.create(user=session['username'], total=total)

    with db.atomic():
        for bread_id, qty in basket.items():
            order_list=OrderList.create(order=order.id, bread=bread_id, quantity=qty)

    session.pop('basket', None)

    return render_template('order.html', bread=bread, basket=basket, total="{0:.2f}".format(total))
