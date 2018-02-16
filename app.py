from flask import Flask, render_template, request, url_for, session
from peewee import DoesNotExist
from views import user, admin, shop
from core import models, api

app = Flask(__name__)
app.config.from_object('core.config.ProductionConfig')
app.register_blueprint(api.app, url_prefix='/api')
app.register_blueprint(user.app)
app.register_blueprint(admin.app, url_prefix='/a')
app.register_blueprint(shop.app)

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

if __name__ == '__main__':
    app.run(debug=True)
