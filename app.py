from flask import Flask, render_template, request, url_for, session
from flask_socketio import SocketIO, emit, send
from peewee import DoesNotExist
from gevent import monkey
from views import user, admin, shop
from core import models, api

import json

monkey.patch_all()

app = Flask(__name__)
app.config.from_object('core.config.ProductionConfig')
app.register_blueprint(api.app, url_prefix='/api')
app.register_blueprint(user.app)
app.register_blueprint(admin.app, url_prefix='/a')
app.register_blueprint(shop.app)

socketio = SocketIO(app)

@app.before_request
def before_request():
    models.initialize()

@app.teardown_request
def teardown_request(exception):
    models.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu/')
def menu():
    try:
        bread=[row for row in models.Bread.select().order_by(models.Bread.name).dicts()]
    except DoesNotExist:
        bread=None
    return render_template('menu.html', bread=bread)

@socketio.on('connect')
def on_connect():
    print('User connected')

@socketio.on('order status', namespace='/admin')
def handle_delivery(message):
    emit('order notification', message, namespace="/{}".format(message['username']), broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
