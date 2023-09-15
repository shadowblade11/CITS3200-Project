from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, logout_user, login_required, login_user
from werkzeug.urls import url_parse

from app import app, db, verification
from app.forms import RegistrationForm, LoginForm, VerificationForm, AdminForm
from app.models import User

import datetime
import os


from app.conversion import convert_to_wav_working_format
from app.produceImage import generate_soundwave_image


@app.route('/')
@app.route('/intro')
def intro():
    return render_template("Intro.html", css="./static/Intro.css")


@app.route('/about')
def about():
    return render_template("About.html", css='./static/About.css')


@app.route('/home')
@login_required
def home():
    return render_template("homePage.html", css='./static/homePage.css')


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
    # print(request.args.get('data')) #way to get folder
    week = request.args.get('data')
    path = f"./app/static/audio/{week}/"
    # print(path)
    audio_clips = os.listdir(path)
    audio_clips = [i.split('.')[0] for i in audio_clips]
    # print(audio_clips)
    # print(current_user)
    #TODO figure how to get current user's id (temp using 123)
    #TODO also once figured out a way to get current user id, use os commands to check if their folder exists, if not, then create it
    return render_template('testPage.html', css='./static/testPage.css', audio_clips=audio_clips, week = week, user="123")

@app.route('/audio-test')
def audio_test():
    return render_template('main.html')

@app.route("/save-audio",methods=['POST'])
def save_audio():
    blob = request.files['blob']
    user = request.form['user']
    week = request.form['week']
    name_of_clip = request.form['name']
    attempt = request.form['attempt']
    name_of_clip = name_of_clip.replace(" ","_")
    PATH_TO_FOLDER = f"./app/static/audio/users/{user}/{week}"
    print("saving clip")

    os.makedirs(PATH_TO_FOLDER,exist_ok=True)

    try:
        blob.save(f"{PATH_TO_FOLDER}/{name_of_clip}-{attempt}-raw.wav")
        print("save successful")
        return 'Upload successful', 200
    except Exception as e:
        print("save failed")
        return str(e), 400
    

@app.route("/send-image",methods=["POST"])
def send_image():
    data = request.json
    name_of_clip = data['name']
    name_of_clip = name_of_clip.replace(" ","_")
    user = data['user']
    week = data['week']
    attempt = data['attempt']
    PATH_TO_AUDIO_FOLDER = f"./app/static/audio/users/{user}/{week}/{name_of_clip}-{attempt}-raw.wav"
    OUTPUT_PATH = f"./app/static/audio/users/{user}/{week}/{name_of_clip}-{attempt}.wav"
    state = convert_to_wav_working_format(PATH_TO_AUDIO_FOLDER,OUTPUT_PATH)
    if state == 0:
        os.remove(PATH_TO_AUDIO_FOLDER)
    else:
        print('something went wrong')


    PATH_TO_IMAGE_FOLDER = f"./app/static/images/users/{user}/{week}"

    os.makedirs(PATH_TO_IMAGE_FOLDER,exist_ok=True)

    image_check = generate_soundwave_image(OUTPUT_PATH,PATH_TO_IMAGE_FOLDER,name_of_clip)

    if image_check == 0:
        return "valid",200

    return "invalid",404

