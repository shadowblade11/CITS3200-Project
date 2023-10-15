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
    
    #relationships
    completed_tests = db.relationship('Complete', backref='user', lazy='dynamic')
    feedback = db.relationship('Feedback', backref='user',lazy='dynamic')
    scores = db.relationship('Score', backref='user',lazy='dynamic')

    def set_passwd(self, passwd):
        self.password_hash = generate_password_hash(passwd)

    def check_passwd(self, passwd):
        return check_password_hash(self.password_hash, passwd)

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(self, username):
        self.username = username

    def avg_score_per_week(self):
        scores = {}

        # Get distinct week numbers
        distinct_weeks = db.session.query(Test.week_number).distinct()
        # distinct_difficulties = db.session.query(Question.difficulty).distinct() # Just going to hardcode difficulties -- saves computation time, is unlikely to change.
        for week in distinct_weeks:  
            week_number = week[0]
            user_scores = self.scores.join(Question).join(Test).filter(Test.week_number == week_number).all()
            if user_scores:
                scores[week_number] = {
                    'user_avg_score': {'all': 0, 'low': 0, 'medium': 0, 'high': 0},
                    'sys_avg_score': {'all': 0, 'low': 0, 'medium': 0, 'high': 0},
                }
                num_scores = {
                    "low": 0,
                    "medium": 0,
                    "high": 0,
                }
                for score in user_scores:
                    question = db.session.query(Question).filter(Question.id == score.question_id).first()
                    scores[week_number]['user_avg_score']['all'] += score.user_score 
                    scores[week_number]['sys_avg_score']['all'] += score.sys_score
                    
                    diff = question.difficulty
                    num_scores[diff] += 1
                    scores[week_number]['user_avg_score'][diff] += score.user_score 
                    scores[week_number]['sys_avg_score'][diff] += score.sys_score
                    
                scores[week_number]['user_avg_score']['all'] /= len(user_scores)
                scores[week_number]['sys_avg_score']['all'] /= len(user_scores)

                for diff in num_scores.keys():
                    if num_scores[diff] > 0 :
                        scores[week_number]['user_avg_score'][diff] /= num_scores[diff]
                        scores[week_number]['sys_avg_score'][diff] /= num_scores[diff]

        return scores
        
    def avg_score_per_test(self):
        avg_scores = {}
        # Get distinct week numbers
        distinct_test = db.session.query(Test.test_name).distinct()
        for test in distinct_test:
            test_name = test[0]
            scores = self.scores
            questions = scores.join(Question)
            tests = questions.join(Test).filter(Test.test_name == test_name)
            # user_scores = tests.all()
            user_scores = self.scores.join(Question).join(Test).filter(Test.test_name == test_name).all()

            if user_scores:
                avg_scores[test_name] = {
                    'user_score': 0,
                    'sys_score': 0,
                }
                
                for score in user_scores:
                    avg_scores[test_name]['user_score'] += score.user_score
                    avg_scores[test_name]['sys_score'] += score.sys_score

                avg_scores[test_name]['user_score'] /= len(user_scores)
                avg_scores[test_name]['sys_score'] /= len(user_scores)

        return avg_scores

@login.user_loader
def load_user(id):
    return User.query.get(id)


class Complete(DB_Queries):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))
    completed = db.Column(db.Boolean)

    def __init__(self, user_id, test_id, status):
        self.id = int(f'{user_id}{test_id}')
        self.user_id = user_id
        self.test_id = test_id
        self.completed = status

    def __repr__(self):
        return f"<Complete (Username: {self.user_id}, Week: {self.test_id}, Completed: {self.completed})>"


class Feedback(DB_Queries):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    feedback = db.Column(db.String(512))
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user_id,test_id,feedback):
        self.id = int(f'{user_id}{test_id}')
        self.feedback = feedback
        self.user_id = user_id
        self.test_id = test_id


class Score(DB_Queries):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_score = db.Column(db.Integer)
    sys_score = db.Column(db.Integer)
    attempt_chosen = db.Column(db.Integer)

    def __init__(self, user_id, question_id,user_score,sys_score,attempt):
        self.id = int(f'{user_id}{question_id}')
        self.user_id = user_id
        self.question_id = question_id
        self.user_score = user_score
        self.sys_score = sys_score
        self.attempt_chosen = attempt

    def __repr__(self):
        return (f'<Score self eval: {self.user_score} , program eval: {self.sys_score} '
                f'(User ID: {self.user_id}, Question ID: {self.question_id})>')

class Test(DB_Queries):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    week_number = db.Column(db.Integer)
    test_name = db.Column(db.String(128))
    due_date = db.Column(db.String(128))  # dd/mm/yy
    number_of_questions = db.Column(db.Integer)

    #relationships
    questions = db.relationship('Question', backref='test',lazy='dynamic')
    completed = db.relationship('Complete', backref='test',lazy='dynamic')
    feedback = db.relationship('Feedback', backref='test',lazy='dynamic')

    def __init__(self, week_no, test_name, due_date, no_of_qs):
        self.test_name = test_name
        self.due_date = due_date
        self.number_of_questions = no_of_qs
        self.week_number = week_no

    def __repr__(self):
        return f'<id: {self.id}, test_name: {self.test_name}, dd: {self.due_date}>'
        # return f'<Test {self.test_name} (Week: {self.week_number})(Questions: {self.questions})>'

    def cohort_average():
        scores = {}

        # Get distinct week numbers
        distinct_weeks = db.session.query(Test.week_number).distinct()
        for week in distinct_weeks:
            week_number = week[0]
            scores_in_week = db.session.query(Score).join(Question).join(Test).filter(Test.week_number == week_number)

            if scores_in_week:
                scores[week_number] = {
                    'user_avg_score': {'all': 0, 'low': 0, 'medium': 0, 'high': 0},
                    'sys_avg_score': {'all': 0, 'low': 0, 'medium': 0, 'high': 0},
                }
                num_scores = {
                    "low": 0,
                    "medium": 0,
                    "high": 0,
                    "all": 0,
                }

                for score in scores_in_week:
                    question = db.session.query(Question).filter(Question.id == score.question_id).first()
                    scores[week_number]['user_avg_score']['all'] += score.user_score 
                    scores[week_number]['sys_avg_score']['all'] += score.sys_score
                    num_scores['all'] += 1

                    diff = question.difficulty
                    num_scores[diff] += 1
                    scores[week_number]['user_avg_score'][diff] += score.user_score 
                    scores[week_number]['sys_avg_score'][diff] += score.sys_score

                if num_scores['all'] > 0:
                    scores[week_number]['user_avg_score']['all'] /= num_scores
                    scores[week_number]['sys_avg_score']['all'] /= num_scores

                for diff in num_scores.keys():
                    if num_scores[diff] > 0 :
                        scores[week_number]['user_avg_score'][diff] /= num_scores[diff]
                        scores[week_number]['sys_avg_score'][diff] /= num_scores[diff]

        return scores
        
    def create_test(self, week_no, test_name, due_date, no_of_qs):
        self.__init__(week_no, test_name, due_date, no_of_qs)



class Question(DB_Queries):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    question_name = db.Column(db.String(128))
    difficulty = db.Column(db.String(10))
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'))

    def __init__(self, question_name, test_id, difficulty):
        self.question_name = question_name
        self.test_id = test_id
        self.difficulty = difficulty

    def __repr__(self):
        return f'<Question {self.question_name} ( Week: {self.test_id}, Difficulty: {self.difficulty})>'
