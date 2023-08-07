from flask_login import current_user, login_user, logout_user

from app import app
from flask import render_template, redirect, url_for
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login', methods= ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # form = LoginForm()
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))