from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, logout_user, login_required, login_user
from werkzeug.urls import url_parse

from app import app, db, verification
from app.forms import RegistrationForm, LoginForm, VerificationForm
from app.models import User


@app.route('/')
@app.route('/home/<int:uid>')
@login_required
def home(uid):
    return render_template("homePage.html")



@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=int(form.id.data)).first()
        print(user)
        if user is None or not user.check_passwd(form.passwd.data):
            flash("Invalid id or password.")
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        session['uid'] = form.id.data
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('loginPage.html', form=form)


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
        return redirect(url_for('verify'))
    return render_template('register.html', form=form, title='Register')


@app.route('/verify', methods=['POST', 'GET'])
def verify():
    form = VerificationForm()
    if request.referrer is None:
        return redirect(url_for('register'))
    if '/'+request.referrer.split(request.host_url)[-1] != url_for('register'):
        return redirect(url_for('register'))
    if 'id' not in session:
        flash("You can only access the verification page from the registration page.")
        return redirect(url_for('register'))

    if request.method == 'POST':
        if session['v_code'] == form.v_code.data:
            user = User(id=session['id'])
            user.set_passwd(session['passwd'])
            session.pop('id')  # Clear the session variable
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            # Verification code doesn't match
            form.v_code.errors = ["Incorrect verification code"]

    return render_template('verify.html', title='Register', form=form)


@app.route('/resend-verification', methods=['POST'])
def resend_verification():
    v_code = verification.generate_v_code(6)
    print(v_code)
    session['v_code'] = v_code # Update verification code
    # verification.send_v_code(session.get('id')+'@student.uwa.edu.au',v_code)
    flash("Verification code has been resent to your email.")
    return redirect(url_for('verify'))
