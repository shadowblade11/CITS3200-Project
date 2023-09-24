import os

from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import current_user, logout_user, login_required, login_user
from werkzeug.urls import url_parse

from app import app, db, verification
from app.forms import RegistrationForm, LoginForm, VerificationForm, AdminForm, ContactForm
from app.models import User

import datetime

from app.conversion import convert_to_wav_working_format
from app.produceImage import generate_soundwave_image




@app.route('/')
@app.route('/intro')
def intro():
    return render_template("Intro.html", css=url_for('static', filename='Intro.css'))


@app.errorhandler(404)
def page_not_found(error):
    return "Oops, page doesn't exist!", 404


@app.route('/about')
def about():
    return render_template("About.html", css=url_for('static', filename='About.css'))


@app.route('/home/<username>')
@login_required
def home(username):
    user = User.query.filter_by(id=username).first_or_404()
    return render_template("homePage.html", css=url_for('static', filename='homePage.css'), username=username)


@app.route('/adminHome', methods=["GET", "POST"])
@login_required
def adminHome():
    return render_template("adminHome.html", css=url_for('static', filename='adminHome.css'))


@app.route('/grades')
def grades():
    return render_template("gradesPage.html", css='./static/gradesPage.css')

@app.route('/contact')
def contact():
    form = ContactForm()
    return render_template('contact.html', form=form, css=url_for('static', filename='contact.css'))


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home', username=current_user.id))  # Provide the username
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.id.data).first()
        if user is None or not user.check_passwd(form.passwd.data) or user.is_admin:
            flash("Invalid id or password.")
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        session['uid'] = form.id.data
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home', username=user.id)
        return redirect(next_page)
    return render_template('loginPage.html', form=form, css=url_for('static', filename='loginPage.css'))


@app.route('/administratorLogin', methods=['GET', 'POST'])
def administratorLogin():
    if (current_user.is_authenticated and
            User.query.filter_by(id=session.get('uid')).first().is_admin):
        return redirect(url_for('adminHome'))  # Provide the username
    form = AdminForm()
    if form.validate_on_submit():
        print(form.username.data)
        user = User.query.filter_by(id=form.username.data).first()
        if user is None:
            return redirect(url_for('administratorLogin'))
        if not user.is_admin or not user.check_passwd(form.passwd.data):
            return redirect(url_for('administratorLogin'))
        login_user(user)
        next_page = request.args.get('next')
        session['uid'] = form.username.data
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('adminHome')
        return redirect(next_page)
    return render_template('adminLogin.html', css=url_for('static', filename='adminLogin.css'), form=form)


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
@app.route('/test/<username>', methods=['GET', 'POST'])
def test(username):
    # print(request.args.get('data')) #way to get folder
    week = request.args.get('data')
    path = f"./app/static/audio/{week}/"
    # print(path)
    audio_clips = os.listdir(path)
    audio_clips = [i.split('.')[0] for i in audio_clips]
    # print(audio_clips)
    # print(current_user)
    # TODO also once figured out a way to get current user id,
    #  use os commands to check if their folder exists, if not, then create it
    return render_template('testPage.html', css=url_for('static', filename='testPage.css'), audio_clips=audio_clips, week=week, user=username)


@app.route('/audio-test')
def audio_test():
    return render_template('main.html')


@app.route("/save-audio", methods=['POST'])
def save_audio():
    blob = request.files['blob']
    user = request.form['user']
    week = request.form['week']
    name_of_clip = request.form['name']
    attempt = request.form['attempt']
    name_of_clip = name_of_clip.replace(" ", "_")
    PATH_TO_FOLDER = f"./app/static/audio/users/{user}/{week}"
    print("saving clip")

    os.makedirs(PATH_TO_FOLDER, exist_ok=True)

    try:
        blob.save(f"{PATH_TO_FOLDER}/{name_of_clip}-{attempt}-raw.wav")
        print("save successful")
        return 'Upload successful', 200
    except Exception as e:
        print("save failed")
        return str(e), 400


@app.route("/send-image", methods=["POST"])
def send_image():
    data = request.json
    name_of_clip = data['name']
    name_of_clip = name_of_clip.replace(" ", "_")
    user = data['user']
    week = data['week']
    attempt = data['attempt']
    PATH_TO_AUDIO_FOLDER = f"./app/static/audio/users/{user}/{week}/{name_of_clip}-{attempt}-raw.wav"
    OUTPUT_PATH = f"./app/static/audio/users/{user}/{week}/{name_of_clip}-{attempt}.wav"
    state = convert_to_wav_working_format(PATH_TO_AUDIO_FOLDER, OUTPUT_PATH)
    if state == 0:
        os.remove(PATH_TO_AUDIO_FOLDER)
    else:
        print('something went wrong')

    PATH_TO_IMAGE_FOLDER = f"./app/static/images/users/{user}/{week}"

    os.makedirs(PATH_TO_IMAGE_FOLDER, exist_ok=True)

    image_check = generate_soundwave_image(OUTPUT_PATH, PATH_TO_IMAGE_FOLDER, name_of_clip)

    if image_check == 0:
        return "valid", 200

    return "invalid", 404


@login_required
@app.route('/addtest', methods=['GET', 'POST'])
def addtest():
    return render_template('adminAddtest.html', css=url_for('static', filename='adminAddtest.css'))


@app.route('/Account')
def Account():
    return render_template("AccountPage.html", css=url_for('static', filename='Account.css'))


@app.route('/start')
def start():
    return render_template("startPage.html", css=url_for('static', filename='startPage.css'))

@app.route('/get-user', methods=['POST'])
def get_user():
    data = request.get_json()
    user = data.get('userID')
    # print(user)
    path = f"./app/static/audio/users/{user}"
    if os.path.exists(path) and os.path.isdir(path):
        wk = os.listdir(path)
        return jsonify({"weeks": wk})
    else:
        return jsonify({"error": "User not found or no audio files"}), 404
    

@app.route('/get-audio', methods=["POST"])
def get_audio():
    data = request.get_json()
    user = data.get('userID')
    week = data.get('week')
    path = f"./app/static/audio/users/{user}/{week}"
    print(path)
    if os.path.exists(path) and os.path.isdir(path):
        clips = os.listdir(path)
        # THIS IS JUST AN EXAMPLE DATA, REPLACE THIS ONCE DB IS IMPLEMENTED
        EXAMPLE_DATA_USER = [5 for i in clips]
        EXAMPLE_DATA_SYS = [8 for i in clips]
        # print(EXAMPLE_DATA_USER)
        return jsonify({"clips":clips,"user_scores":EXAMPLE_DATA_USER,"sys_scores": EXAMPLE_DATA_SYS})
    return jsonify({"error":"No audio files"}),404

@app.route('/save-feedback',methods=["POST"])
def save_feedback():
    data = request.get_json()
    text = data.get('txt')
    week = data.get('week')
    user = data.get('user')
    #THIS IS WHERE WE CAN STORE THE FEEDBACK
    try:
        # REPLACE THIS WITH THE TABLE ASSIGNMENT
        print(f'The Text is {text}\nThe User who did the test is {user}\nThe Week that the test was in is {week}')
        return "passed",200
    except:
        return "failed",404












# @app.route('/test')
# def testPage():
#     return render_template("testPage.html", css=url_for('static', filename='testPage.css'))
