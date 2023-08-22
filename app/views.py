from app import app
from flask import render_template, request

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/test')
def test():
    return render_template('main.html')


@app.route("/save-audio",methods=['POST'])
def save_audio():
    data = request.data
    # print(f'this is the {data}')
    with open("sound.wav",'ab') as f:
        f.write(data)
    return "temp"

