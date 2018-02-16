from flask import Blueprint, request, url_for, jsonify
from core.models import Order

app=Blueprint('api', __name__)

@app.route('/order/change_status', methods=['POST'])
def order_change_status():
    return jsonify(Order.update(status=request.form['status']).where(Order.id==request.form['id']).execute() != 0)