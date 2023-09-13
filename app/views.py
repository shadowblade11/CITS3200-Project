from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, logout_user, login_required, login_user
from werkzeug.urls import url_parse

from app import app, db, verification
from app.forms import RegistrationForm, LoginForm, VerificationForm, AdminForm, ContactForm
from app.models import User

import datetime


@app.route('/')
@app.route('/intro')
def intro():
    return render_template("Intro.html", css="./static/Intro.css")


@app.route('/about')
def about():
    return render_template("About.html", css='./static/About.css')

@app.route('/adminLogin')
def admin():
    return render_template("adminLogin.html", css='./static/adminLogin.css')

@app.route('/home')
@login_required
def home():
    return render_template("homePage.html", css='./static/homePage.css')

@app.route('/contact')
def contact():
    form = ContactForm()
    return render_template('contact.html', form=form, css='./static/contact.css')

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=int(form.id.data)).first()
        print(user)
        if user is None or not user.check_passwd(form.passwd.data) or user.is_admin:
            flash("Invalid id or password.")
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        session['uid'] = form.id.data
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('loginPage.html', form=form, css='./static/loginPage.css')


@app.route('/administratorLogin', methods=['GET', 'POST'])
def administratorLogin():
    form = AdminForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.username.data).first()
        if not user.is_admin or user.check_passwd(form.passwd.data):
            return redirect(url_for('login'))

        # TODO: check passwd
    return render_template('adminLogin.html', css='./static/adminLogin.css', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(id=int(form.id.data)).first() is not None:
            message = "ID already exists."
            return render_template('register.html', form=form, title='Register', message=message)
        session['id'] = form.id.data
        session['passwd'] = form.passwd2.data
        v_code = verification.generate_v_code(6)
        # verification.send_v_code(form.id.data+'@student.uwa.edu.au', v_code)
        print(v_code)
        session['v_code'] = v_code
        session['start_time'] = datetime.datetime.now()
        return redirect(url_for('verify'))
    return render_template('register.html', form=form, title='Register')


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    form = VerificationForm()

    if request.method == 'POST':
        if session['v_code'] != form.v_code.data and (
                datetime.datetime.now() - session['start_time']).total_seconds() > 60:
            # Verification code doesn't match
            form.v_code.errors = ["Incorrect verification code"]
        elif session['v_code'] == form.v_code.data:
            user = User(id=session['id'])
            user.set_passwd(session['passwd'])
            print(user)
            session.pop('id')  # Clear the session variable
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

        if request.referrer is None:
            return redirect(url_for('register'))
        if '/' + request.referrer.split(request.host_url)[-1] != url_for('register'):
            return redirect(url_for('register'))
        if 'id' not in session:
            flash("You can only access the verification page from the registration page.")
            return redirect(url_for('register'))

    return render_template('verify.html', title='Register', form=form)


@app.route('/resend-verification', methods=['POST'])
def resend_verification():
    v_code = verification.generate_v_code(6)
    print(v_code)
    session['v_code'] = v_code  # Update verification code
    # verification.send_v_code(session.get('id')+'@student.uwa.edu.au',v_code)
    flash("Verification code has been resent to your email.")
    return redirect(url_for('verify'))


@login_required
@app.route('/test', methods=['GET', 'POST'])
def test():
    return render_template('testPage.html', css='./static/testPage.css')

@app.route('/Account')
def Account():
    return render_template("AccountPage.html", css='./static/Account.css')

@app.route('/start')
def start():
    return render_template("startPage.html", css='./static/startPage.css')

@app.route('/test')
def testPage():
    return render_template("testPage.html", css='./static/testPage.css')
