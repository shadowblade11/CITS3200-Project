from flask_login import UserMixin
from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import SQLAlchemyError


class DatabaseException(Exception):
    def __init__(self, message="A database-related error occurred."):
        self.message = message
        super().__init__(self.message)


class DB_Queries(db.Model):
    __abstract__ = True

    @classmethod
    def get(cls, **kwargs):  # Return a single object
        try:
            return cls.query.filter_by(**kwargs).first()
        except SQLAlchemyError as e:
            # Handle the exception (e.g., log it, raise a custom exception, etc.)
            raise DatabaseException("Error while retrieving data from the database.") from e

    @classmethod
    def get_all(cls, **kwargs):  # Return a list of objects
        try:
            return cls.query.filter_by(**kwargs).all()
        except SQLAlchemyError as e:
            # Handle the exception
            raise DatabaseException("Error while retrieving data from the database.") from e

    @classmethod
    def view_all(cls):
        try:
            return cls.query.all()
        except SQLAlchemyError as e:
            # Handle the exception
            raise DatabaseException("Error while retrieving data from the database.") from e

    @classmethod
    def write_to(cls, obj):
        try:
            db.session.add(obj)
            db.session.commit()
        except SQLAlchemyError as e:
            # Handle the exception
            db.session.rollback()  # Rollback the transaction in case of an error
            raise DatabaseException("Error while writing data to the database.") from e


class User(UserMixin, DB_Queries):
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


@login.user_loader
def load_user(id):
    return User.query.get(id)


class Test(DB_Queries):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer)
    user_id = db.Column(db.String, db.ForeignKey('user.id'),
                        name='fk_test_user_id')
    questions = db.relationship('Question', backref='test', lazy='dynamic')
    feedback = db.Column(db.String(512))

    def __repr__(self):
        return f'<Test {self.test_id} (User ID: {self.user_id}),Feedback:{self.feedback}>'

    def __init__(self, test_id, user_id):
        self.test_id = test_id
        self.user_id = user_id
        self.feedback = None


class Question(DB_Queries):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer)
    difficulty = db.Column(db.Integer)
    self_evaluation = db.Column(db.Integer)
    program_evaluation = db.Column(db.Integer)
    user_id = db.Column(db.String, db.ForeignKey('user.id'))
    test_id = db.Column(db.Integer, db.ForeignKey('test.test_id'))

    def __repr__(self):
        return ('<Question {} (User ID: {}, Test ID: {})>'
                .format(self.question_id, self.user_id, self.test_id))

    def __init__(self, question_id, user_id, test_id, difficulty):
        self.program_evaluation, self.self_evaluation, self.teacher_evaluation = 0, 0, 0
        self.question_id = question_id
        self.user_id = user_id
        self.test_id = test_id
        self.difficulty = 6

