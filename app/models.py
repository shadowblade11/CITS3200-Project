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
    def write_to(cls, obj):
        try:
            db.session.add(obj)
            db.session.commit()
        except SQLAlchemyError as e:
            # Handle the exception
            db.session.rollback()  # Rollback the transaction in case of an error
            raise DatabaseException("Error while writing data to the database.") from e


class User(UserMixin, DB_Queries):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)
    # completed_tests = db.relationship('Complete', backref='user')
    # feedback = db.relationship('Feedback', backref='user')

    def set_passwd(self, passwd):
        self.password_hash = generate_password_hash(passwd)

    def check_passwd(self, passwd):
        return check_password_hash(self.password_hash, passwd)

    def __repr__(self):
        # return f'<id {self.id}, username {self.username}, password_hash {self.password_hash}, is_admin {self.is_admin}, completed tests {self.completed_tests}, feedback {self.feedback}>'
        return f'<id {self.id}, username {self.username}, password_hash {self.password_hash}, is_admin {self.is_admin}>'

    # def __init__(self, id):
    #     self.id = id


@login.user_loader
def load_user(id):
    return User.query.get(id)

class Test(DB_Queries):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    week_number = db.Column(db.Integer)
    test_name = db.Column(db.String(128))
    due_date = db.Column(db.String(128))  # dd/mm/yy
    number_of_questions = db.Column(db.Integer)
    # questions = db.relationship('Question', backref='test')
    def __repr__(self):
        return f'<id {self.id}, wk {self.week_number}, testname {self.test_name}>'

# class Complete(DB_Queries):
#     completed_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
#     test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
#     # user = db.relationship('User', backref='complete')
#     completed = db.Column(db.Boolean)

#     # def __init__(self, user):
#     #     self.user_id = user
#     #     self.completed = False
#     def __repr__(self):
#         return f'<id {self.completed_id}, user_id {self.user_id}, test_id {self.test_id}, completed {self.completed}>'


# class Feedback(DB_Queries):
#     feedback_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     feedback = db.Column(db.String(512))
#     test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
#     user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
#     # user = db.relationship('User', backref='feedback')
#     def __repr__(self):
#         return f'<id {self.feedback_id}, feedback {self.feedback}, test_id {self.test_id}, user_id {self.user_id}>'
#     # def __init__(self, user):
#     #     self.feedback = None
#     #     self.user_id = user


# class Score(DB_Queries):
#     score_id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
#     user_score = db.Column(db.Integer)
#     sys_score = db.Column(db.Integer)
#     attempt_chosen = db.Column(db.Integer)

#     def __repr__(self):
#         return f'<score_id {self.score_id}, user_id {self.user_id}, question_id {self.question_id}, user_score {self.user_score}, etc>'
#     # def __init__(self, user):
#     #     self.sys_score, self.user_score, self.attempt_chosen = 0, 0, 0
#     #     self.user_id = user

#     # def __init__(self, week_no, test_name, due_date, no_of_qs):
#     #     self.test_name = test_name
#     #     self.due_date = due_date
#     #     self.number_of_questions = no_of_qs
#     #     self.week_number = week_no


# class Question(DB_Queries):
#     id = db.Column(db.Integer, primary_key=True,autoincrement=True)
#     question_name = db.Column(db.String(128))
#     difficulty = db.Column(db.Integer)
#     test_id = db.Column(db.Integer, db.ForeignKey('test.id'))

#     def __repr__(self):
#         return f'<id {self.id}, test_id {self.test_id}>'
#     # def __init__(self, question_name, test_id, difficulty):
#     #     self.question_name = question_name
#     #     self.test_id = test_id
#     #     self.difficulty = difficulty
