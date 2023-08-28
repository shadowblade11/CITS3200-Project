from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/About')
def about():
    return render_template('About.html')

@app.route('/Account')
def account():
    return render_template('AccountPage.html')

@app.route('/Intro')
def intro():
    return render_template('Intro.html')