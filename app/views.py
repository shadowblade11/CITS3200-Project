from flask_login import current_user, login_user, logout_user
from wtforms import ValidationError

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
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form1 = RegistrationForm()
    form2 = VerificationForm()
    if request.method == 'POST':
        if form2.validate_on_submit():
            v_code = verification.generate_v_code(6)  # Generate verification code for user
            print(v_code)
            session['verification_code'] = v_code
            # verification.send_v_code(email_addr=rForm.id.data + '@student.uwa.edu.au', v_code=v_code)
            flash("Verification code has been sent to your email. "
                  "Please check your inbox or junk folder and enter the code.")
        if form1.validate_on_submit():
            if session['verification_code'] == form1.v_code.data:
                # TODO: check user's verification code
                user = User(id=form1.id.data)
                user.set_passwd(form1.passwd1.data)
                return redirect(url_for('login'))
            else:
                print("doesnt match")
                form1.v_code.errors = list(form1.v_code.errors)
                form1.v_code.errors.append("Incorrect verification code")  # Add an error message to the form field
        # db.session.add(user)
        # db.session.commit()  # Get the data user submitted and write into the database
        # flash("Registration successful!")
        # return url_for('login')
    return render_template('register.html', title='Register', form1=form1, form2=form2)


