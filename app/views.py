from flask_login import current_user, login_user, logout_user

from app import app, db, verification
from flask import render_template, redirect, url_for, flash, request, session

from app.forms import RegistrationForm, LoginForm, VerificationForm
from app.models import User


@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/')
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User(id=form.id.data)
        user.set_passwd(passwd=form.passwd.data)
        print(user.check_passwd("1234"))
        return redirect(url_for('index'))
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    return render_template('loginPage.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        session['id'] = form.id.data
        session['passwd'] = form.passwd2.data
        v_code = verification.generate_v_code(6)
        print(v_code)
        session['v_code'] = v_code
        return redirect(url_for('verify'))
    return render_template('register.html', form=form, title='Register')


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    form = VerificationForm()

    if 'id' not in session:
        flash("You can only access the verification page from the registration page.")
        return redirect(url_for('register'))

    if request.method == 'POST':
        if session['v_code'] == form.v_code.data:
            user = User(id=session['id'])
            user.set_passwd(session['passwd'])
            session.pop('id')  # Clear the session variable
            return redirect(url_for('login'))
        else:
            # Verification code doesn't match
            form.v_code.errors = ["Incorrect verification code"]

    return render_template('verify.html', title='Register', form=form)

