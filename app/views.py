import os

from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import current_user, logout_user, login_required, login_user
from werkzeug.urls import urlsplit
from werkzeug.utils import secure_filename

from app import app, verification
import app.interact_database as db
from app.forms import RegistrationForm, LoginForm, VerificationForm, AdminForm, ContactForm
from app.models import *

import datetime


from app.conversion import convert_to_wav_working_format
from app.produceImage import generate_soundwave_image

from app.interact_database import *


import random 


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
    user = User.query.filter_by(username=username).first_or_404()

    completed_tests = user.completed_tests.all()
    all_tests = Test.get_all()
    completed_tests = [i.test_id for i in completed_tests]
    all_tests = [i.id for i in all_tests]

    tests_to_do_id = list(set(all_tests)-set(completed_tests))
    tests_to_do = []
    for i in tests_to_do_id:
        tests_to_do.append(Test.get(id=i).test_name)
    print(tests_to_do)
    return render_template("homePage.html", css=url_for('static', filename='homePage.css'), username=username, tests_to_do=tests_to_do)


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
        return redirect(url_for('home', username=current_user.username))  # Provide the username
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(username=form.id.data)
        if user is None or not user.check_passwd(form.passwd.data) or user.is_admin:
            flash("Invalid id or password.")
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        session['uid'] = form.id.data
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('home', username=user.username)
        return redirect(next_page)
    return render_template('loginPage.html', form=form, css=url_for('static', filename='loginPage.css'))


@app.route('/administratorLogin', methods=['GET', 'POST'])
def administratorLogin():
    if (current_user.is_authenticated and
            User.query.filter_by(username=current_user.username).is_admin):
        return redirect(url_for('adminHome'))  # Provide the username
    form = AdminForm()
    if form.validate_on_submit():
        user = User.get(username= form.username.data)
        if user is None:
            return redirect(url_for('administratorLogin'))
        if not user.is_admin or not user.check_passwd(form.passwd.data):
            return redirect(url_for('administratorLogin'))
        login_user(user)
        next_page = request.args.get('next')
        session['uid'] = form.username.data
        if not next_page or urlsplit(next_page).netloc != '':
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
        if User.get(username=form.id.data) is not None:
            message = "Username already exists."
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
            user = User(username=session['id'])
            user.set_passwd(session['passwd'])
            user.is_admin = False
            session.pop('id')  # Clear the session variable
            User.write_to(user)
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
    return render_template('testPage.html', css=url_for('static', filename='testPage.css'), audio_clips=audio_clips,
                           week=week, user=username)


@app.route("/save-audio", methods=['POST'])
def save_audio():
    blob = request.files['blob']
    user = request.form['user']
    test_name = request.form['test_name']
    name_of_clip = request.form['name']
    attempt = request.form['attempt']
    # name_of_clip = name_of_clip.replace(" ", "_")
    PATH_TO_FOLDER = f"./app/static/audio/users/{user}/{test_name}"
    PATH_TO_IMAGE_FOLDER = f"./app/static/images/users/{user}/{test_name}"
    print("saving clip")

    os.makedirs(PATH_TO_FOLDER, exist_ok=True)
    os.makedirs(PATH_TO_IMAGE_FOLDER, exist_ok=True)

    try:
        raw_file = f"{PATH_TO_FOLDER}/{name_of_clip}-{attempt}-raw.wav"
        clean_file = f"{PATH_TO_FOLDER}/{name_of_clip}-{attempt}.wav"
        blob.save(raw_file)
        print("save successful")

        convert_to_wav_working_format(raw_file,clean_file)

        os.remove(raw_file)
        
        print("saving image")
        generate_soundwave_image(clean_file, PATH_TO_IMAGE_FOLDER, f'{name_of_clip}-{attempt}')
        print("save successful")

        return 'Upload successful', 200
    except Exception as e:
        print("save failed")
        return str(e), 400


@app.route('/calculate-score', methods=['POST'])
def calculate_score():
    user = request.form['user']
    test_name = request.form['test_name']
    name_of_clip = request.form['name']
    attempt = request.form['attempt']
    user_score = request.form['user_score']

    PATH_TO_USER_ATTEMPT = f"./app/static/audio/users/{user}/{test_name}/{name_of_clip}-{attempt}.wav"
    PATH_TO_SOURCE = f"./app/static/audio/{test_name}/{name_of_clip}.wav"

    print(PATH_TO_USER_ATTEMPT)
    print(PATH_TO_SOURCE)

    score = random.randrange(0,100)
    # score = similarity_function(PATH_TO_SOURCE, PATH_TO_USER_ATTEMPT)
    print(f"User Score = {user_score}, Actual Score = {score}")
    user_id = User.get(username=user).id
    test_id = Test.get(test_name=test_name).id
    question_id = Question.get(test_id=test_id,question_name=name_of_clip).id
    s = Score(user_id=user_id,question_id=question_id,user_score=user_score,sys_score=score,attempt=attempt)
    Score.write_to(s)
    #MAKE SCORE OBJECT WITH user_score and score

    questions_completed = User.get(id=user_id).scores.all()
    questions_completed = [i.question_id for i in questions_completed]
    test_questions = Test.get(id=test_id).questions.all()
    test_questions = [i.id for i in test_questions]

    count = 0

    for i in test_questions:
        if i in questions_completed:
            count = count +1
    print(Test.get(id=test_id).number_of_questions)
    print(count)
    if count == Test.get(id=test_id).number_of_questions:
        c = Complete(user_id=user_id,test_id=test_id,status=True)
        Complete.write_to(c)
    return str(score),200

@login_required
@app.route('/addtest', methods=['GET', 'POST'])
def addtest():
    if not current_user.is_admin:
        return redirect(url_for('page_not_found'))
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
    
    
@app.route('/get-user-marks', methods=['POST'])
def get_user_marks():
    data = request.get_json()
    user = data.get('userID')
    try:
        user_id = User.get(username=user).average_score_per_week()
        print(user_id)
        return jsonify(user_id), 200
    except:
        return "", 404


@app.route('/get-test-marks', methods=['POST'])
def get_test_marks():
    try:
        test = Test.get(test_name="asdf")
        print(test)
        averages = test.average_scores_per_test_per_week()
        print(jsonify(averages))
        return jsonify(averages), 200
    except:
        return "", 404


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
    test_name = data.get('week')
    user = data.get('user')
    print(user)
    print(text)
    # print(week)
    # week = int(week[-1])
    #THIS IS WHERE WE CAN STORE THE FEEDBACK
    try:
        # REPLACE THIS WITH THE TABLE ASSIGNMENT
        user_id = User.get(username=user).id
        test_id = Test.get(test_name=test_name).id
        f = Feedback.get(user_id=user_id,test_id=test_id)
        if f is None:
            f = Feedback(user_id=user_id,test_id=test_id,feedback=text)
            Feedback.write_to(f)
            return "passed",200
        f.feedback = text
        Feedback.write_to(f)
        # print(f'The Text is {text}\nThe User who did the test is {user}\nThe Week that the test was in is {week}')
        return "passed",200
    except:
        return "failed",404



@app.route('/get-feedback',methods=["GET"])
def send_feedback():
    user = request.args.get('user')
    test_name = request.args.get('week')
    # print(f"User: {user}, Week: {week}")
    # THIS IS WHERE WE RETRIVE FEEDBACK FROM THE DATABASE

    #FAKE DATA
    # data = {
    # "123": {
    #     'week1': 'This is a random sentence for week 1.',
    #     'week2': 'Here is a different sentence for week 2.',
    #     'week3': 'Week 3 has its own unique sentence as well.'
    # }
    # }
    try:
        user_id = User.get(username=user).id
        test_id = Test.get(test_name=test_name).id
        txt = Feedback.get(user_id=user_id,test_id=test_id).feedback
        # string = data[user][week]
        return txt,200
    except:
        return "", 404


UPLOAD_FOLDER = 'app/static/audio'

@app.route('/upload_files', methods=['POST'])
def upload_files():
    try:
        test_name = request.form.get('testName')
        due_date = request.form.get('dueDate')
        week_number = request.form.get('weekNumber')
        TEST_LOCATION_FOLDER = f"{UPLOAD_FOLDER}/{test_name}" 
        if not os.path.exists(TEST_LOCATION_FOLDER):
            os.makedirs(TEST_LOCATION_FOLDER)
        if not os.path.exists(f"app/static/images/{test_name}"):
            os.makedirs(f"app/static/images/{test_name}")
        n_of_qs = 0
        difficulty_levels = ['low', 'medium', 'high']
        for difficulty in difficulty_levels:
            file_key = f'{difficulty}DifficultyFile'
            if file_key in request.files:
                files = request.files.getlist(file_key)
                for file in files:
                    if file:
                        n_of_qs = n_of_qs + 1


        test = Test(week_no = int(week_number), test_name=test_name,due_date=due_date,no_of_qs=n_of_qs)
        Test.write_to(test)
        uploaded_files = {}
        for difficulty in difficulty_levels:
            file_key = f'{difficulty}DifficultyFile'
            if file_key in request.files:
                files = request.files.getlist(file_key)
                file_paths = []
                selected_files = []
                for file in files:
                    if file:
                        name, suffix = file.filename.split('.')
                        filename = os.path.join(TEST_LOCATION_FOLDER, f"{name}-raw.{suffix}")
                        # print(file.filename)
                        file.save(filename)
                        # print(filename)
                        formatted_name = name.replace(' ','_')
                        OUTPUT_FILE = f"{TEST_LOCATION_FOLDER}/{formatted_name}.wav"
                        convert_to_wav_working_format(filename,OUTPUT_FILE)
                        os.remove(filename)
                        generate_soundwave_image(OUTPUT_FILE,f"app/static/images/{test_name}",formatted_name)
                        file_paths.append(OUTPUT_FILE)
                        selected_files.append(formatted_name)
                        question = Question(question_name=formatted_name,difficulty=difficulty,test_id=test.id)
                        Question.write_to(question)
                uploaded_files[difficulty] = file_paths
                print(f"Difficulty : {difficulty} File : {', '.join(selected_files)}")
        print(f"Test Name : {test_name}")
        print(f"Week number : {week_number}")
        print(f"Due date : {due_date}")
        print(f"Number of Questions : {n_of_qs}")
        return jsonify(uploaded_files), 200
    except Exception as e:
        print(e)
        return str(e), 500




# @app.route('/test')
# def testPage():
#     return render_template("testPage.html", css=url_for('static', filename='testPage.css'))
