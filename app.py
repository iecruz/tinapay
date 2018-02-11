from flask import Flask, render_template, request, url_for, session
from views import users, admin, shop
from core import models

app = Flask(__name__)
app.config.from_object('core.config.ProductionConfig')
app.register_blueprint(users.app)
app.register_blueprint(admin.app, url_prefix='/access')
app.register_blueprint(shop.app)

@app.before_request
def before_request():
    models.initialize()

@app.teardown_request
def teardown_request(exception):
    models.close()

@app.route('/')
def index():
    return render_template('index.html', app=app.config)

if __name__ == '__main__':
    app.run()
