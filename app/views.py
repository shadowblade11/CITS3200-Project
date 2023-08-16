from flask_login import current_user, login_user, logout_user
from wtforms import ValidationError

from app import app, db, verification
from flask import render_template, redirect, url_for, flash, request, session

from app.forms import RegistrationForm, LoginForm
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
        if form.submit.data:
            if form.id.data and form.passwd.data:
                user = User(id=form.id.data)
                user.set_passwd(passwd=form.passwd.data)
                print(user.check_passwd("1234"))
                return redirect(url_for('index'))
            else:
                flash("Please fill in both fields to sign in.")
    if current_user.is_authenticated:
        return render_template("index.html")
    return render_template('loginPage.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if request.form.get('send_verification'):  # user requests for verification code
            v_code = verification.generate_v_code(6)  # Generate verification code for user
            print(v_code)
            session['verification_code'] = v_code
            # verification.send_v_code(email_addr=form.id.data + '@student.uwa.edu.au', v_code=v_code)
            flash("Verification code has been sent to your email. "
                  "Please check your inbox or junk folder and enter the code.")
        if request.form.get('submit'):
            if session['verification_code'] == form.v_code.data:
                # TODO: check user's verification code
                user = User(id=form.id.data)
                user.set_passwd(form.passwd1.data)
                return redirect(url_for('login'))
            else:
                print("doesnt match")
                form.v_code.errors = list(form.v_code.errors)
                form.v_code.errors.append("Incorrect verification code")  # Add an error message to the form field
        # db.session.add(user)
        # db.session.commit()  # Get the data user submitted and write into the database
        # flash("Registration successful!")
        # return url_for('login')
    return render_template('register.html', title='Register', form=form)


