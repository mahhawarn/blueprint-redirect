from flask import Blueprint, render_template
from models import db, User

from flask_login import LoginManager
from flask import Blueprint, render_template, redirect, url_for, flash
from applications.login.forms import LoginForm, SignUpForm
from flask_login import login_user, logout_user, login_required

#Blueprint
login_bp = Blueprint('login_app', __name__, url_prefix="/applications/login")

@login_bp.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username = username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            return redirect(url_for("index"))
        flash("認証不備です")
    return render_template("login/login_form.html", form=form)

@login_bp.route("/register", methods=["GET", "POST"])
def register():
    # Formインスタンス生成
    form = SignUpForm()
    if form.validate_on_submit():
        # データ入力取得
        username = form.username.data
        password = form.password.data
        # モデルを生成
        user = User(username=username)
        # パスワードハッシュ化 model内の関数 user.の
        user.set_password(password)
        # 登録処理
        db.session.add(user)
        db.session.commit()
        # フラッシュメッセージ
        flash("ユーザー登録しました")
        # 画面遷移
        return redirect(url_for("login_app.login"))
    # GET時
    # 画面遷移
    return render_template("login/register_form.html", form=form)
