from flask import Flask, render_template, abort, redirect, url_for
from flask_migrate import Migrate
from models import db, User, URLList

from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required

#blueprint
from applications.login.views import login_bp
from applications.redirect.views import redirect_bp


app = Flask(__name__)

# DB
app.config.from_object("config.Config")
db.init_app(app)
migrate = Migrate(app, db)

# login設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "認証していません：ログインしてください"
login_manager.login_view = 'login_app.login'

# Blueprint
app.register_blueprint(login_bp)
app.register_blueprint(redirect_bp)

@app.route('/')
def index():
    return redirect(url_for("redirect_app.input"), code=301)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from errorhandler import *

if __name__ == "__main__":
    app.run()
