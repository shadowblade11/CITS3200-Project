from flask_login import current_user, login_user, logout_user

from app import app, db, verification
from flask import render_template, redirect, url_for, flash, request

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
            user = User(id=form.id.data, passwd=form.passwd.data)
            print(user)
            # User.check_passwd(form.passwd.data,"1234")
            return redirect(url_for('index'))
        elif form.register.data:
            return redirect(url_for('register'))
    if current_user.is_authenticated:
        return render_template("index.html")
    return render_template('loginPage.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if request.form.get('send_verification') and not form.id.data is None:  # user requests for verification code
            v_code = verification.generate_v_code(6)  # Generate verification code for user
            verification.send_v_code(email_addr=form.id.data + '@student.uwa.edu.au', v_code=v_code)
            flash("Verification code has been sent to your email. "
                  "Please check your inbox or junk folder and enter the code.")
        user = User(id=form.id.data)
        user.set_passwd(form.passwd1.data)
        db.session.add(user)
        db.session.commit()  # Get the data user submitted and write into the database
        flash("Registration successful!")
        return url_for('login')
    return render_template('register.html', title='Register', form=form)
