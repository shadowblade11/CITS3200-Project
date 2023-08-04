# from flask_login import current_user, login_required, login_user, logout_user
from app import app
from flask import redirect, render_template, url_for

@app.route('/')
@app.route('/index')
# @login_required
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    # if current_user.is_authenticated:
    # return redirect(url_for('index'))
    # else:
    return render_template('signup.html')


@app.route('/login')
def login():
    # if current_user.is_authenticated:
    # return redirect(url_for('index'))
    # else:
    return render_template('login.html')
