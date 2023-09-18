from flask_login import UserMixin
from app import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.String, primary_key=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    tests = db.relationship('Test', backref='user', lazy='dynamic')

    def set_passwd(self, passwd):
        self.password_hash = generate_password_hash(passwd)

    def check_passwd(self, passwd):
        return check_password_hash(self.password_hash, passwd)

    def __repr__(self):
        return f'<User {self.id}>'

    def __init__(self, id):
        self.is_admin = False
        self.id = id


class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer)
    user_id = db.Column(db.String, db.ForeignKey('user.id'),
                        name='fk_test_user_id')  # Provide a name for the foreign key
    questions = db.relationship('Question', backref='test', lazy='dynamic')

    def __repr__(self):
        return f'<Test {self.test_id} (User ID: {self.user_id})>'


# Use "test_1 = Test(test_id=1, user_id='123')" to create a week 1 test for user 123
# Use "tests = Test.query.filter_by(user_id="userID", test_id= 1).all()" to get the test 1 associated to the user

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    self_evaluation = db.Column(db.Integer)
    teacher_evaluation = db.Column(db.Integer)
    program_evaluation = db.Column(db.Integer)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    test_id = db.Column(db.Integer, db.ForeignKey('test.test_id'))
    feedback = db.Column(db.String(256))

    def __repr__(self):
        return ('<Feedback of Question {} (User ID: {}, Test ID: {}): {}>'
                .format(self.question_id, self.user_id, self.test_id, self.feedback))

    def __init__(self, question_id, user_id, test_id):
        self.program_evaluation, self.self_evaluation, self.teacher_evaluation = 0, 0, 0
        self.feedback = None
        self.question_id = question_id
        self.user_id = user_id
        self.test_id = test_id

# Use questions = Question.query.filter_by(test_id=2, user_id='123').all()
# to find the questions associated with user 123's 2nd test

# Use question = Question(question_id=2, test_id=2, user_id='123') to create a question for user 123 in test 2
