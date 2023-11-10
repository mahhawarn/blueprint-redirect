from flask import Flask, render_template, abort, send_file, redirect, url_for, flash
from flask import session, Blueprint
from datetime import timedelta
from flask_migrate import Migrate
from models import db, URLList
from bs4 import BeautifulSoup
from applications.redirect.forms import InputForm
import urllib.request, urllib.error
import os

from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required

# Blueprint
redirect_bp = Blueprint('redirect_app', __name__, url_prefix="/applications/redirect")

# URLタイトル取得関数
def url_title_get(url):
    response = urllib.request.urlopen(url)
    parse_html = BeautifulSoup(response, "html.parser")
    title = parse_html.title.string
    return title

# URL取得関数
def url_get(id):
    urls = URLList.query.filter_by(id=id).first()
    urlstr = urls.url_str
    if urlstr == None:
        return redirect(url_for("redirect_app.input"), code=301)
    else:
        return urlstr

# ID取得関数 要素数カウント
def urlid_get():
    count = URLList.query.count()
    getid = count
    if getid == None:
        return redirect(url_for("redirect_app.input"), code=301)
    else:
        return getid

# 短縮URL変換関数
def url_change(id):
    urlstr = ("http://127.0.0.1:5000/applications/redirect/redirect/"+str(id))
    return urlstr

@redirect_bp.route('/input', methods=['GET','POST'])
@login_required
def input():
    form = InputForm()
    session['url'] = None
    if form.validate_on_submit():
        url_str = form.url.data
        urls = URLList(url_str=url_str)
        session['url'] = url_str
        db.session.add(urls)
        db.session.commit()
        flash("URL登録完了")
        return redirect(url_for("redirect_app.download_api"), code=301)
    return render_template("redirect/home.html", form=form)

@redirect_bp.route('/redirectgo')
def redirect_func():
    url = session['url']
    if url == None:
        return redirect(url_for("redirect_app.input"))
    else:
        return redirect(url, code=301)

@redirect_bp.route('/redirect/<int:id>')
def id_redirect(id):
    url = url_get(id)
    return redirect(url, code=301)

@redirect_bp.route("/download", methods=["GET", 'POST'])
@login_required
def download_api():
    os.remove("short_url.txt")
    with open('short_url.txt', 'w') as f:
        id = urlid_get()
        str = url_get(id)
        title = url_title_get(str)
        short_url = url_change(id)
        f.write("タイトル:"+title)
        f.write("\n")
        f.write("URL:"+"\n")
        f.write(short_url+"\n")
        pass
    filepath = "./short_url.txt"
    filename = os.path.basename(filepath)
    sd = send_file(filepath, as_attachment=True, mimetype='text/plain')
    return sd
