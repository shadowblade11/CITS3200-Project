from flask_login import UserMixin

from app import db, login
from werkzeug.security import check_password_hash, generate_password_hash


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)

    def set_passwd(self, passwd):
        self.password_hash = generate_password_hash(passwd)

    def check_passwd(self, passwd):
        return check_password_hash(self.password_hash, passwd)

    def __repr__(self):
        return f'<User {self.id}>'

    # def __init__(self,id):
    #     self.password_hash = None
    #     self.id = id
    #     self.is_admin = False


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
# class Test(UserMixin, db.Model):
#     pass
