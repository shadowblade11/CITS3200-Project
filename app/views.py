from flask_login import current_user, login_user, logout_user

from app import app, db, verification
from flask import render_template, redirect, url_for, flash, request

from app.forms import RegistrationForm
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # form = LoginForm()
    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return url_for('index')
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.form.get('send_verification') and not form.id.data is None:  # user requests for verification code
            v_code = verification.generate_v_code(6)  # Generate verification code for user
            verification.send_v_code(email_addr=form.id.data+'@student.uwa.edu.au', v_code=v_code)
            flash("Verification code has been sent to your email. "
                  "Please check your inbox or junk folder and enter the code.")
        user = User(id=form.id.data)
        user.set_passwd(form.passwd1.data)
        db.session.add(user)
        db.session.commit() # Get the data user submitted and write into the database
        flash("Registration successful!")
        return url_for('login')
    return render_template('register.html', title='Register', form=form)
