# from flask_login import LoginManager
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

DB_NAME = "database.db"    

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

app.app_context().push()


# Database
# Required for SQLite
# convention = {
#     "ix": 'ix_%(column_0_label)s',
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(constraint_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s"
# }

# metadata = MetaData(naming_convention=convention)
# db = SQLAlchemy(app, metadata=metadata)
# migrate = Migrate(app, db, render_as_batch=True)

# login_manager = LoginManager()
# login_manager.init_app(app)

# from app.models import User

# @login_manager.user_loader
# def load_user(id):
#     return db.session.query(User).get(int(id))

# @login_manager.unauthorized_handler
# # route on not logged in
# def unauthorized():
#     return redirect("/login", code=302)

from app import views  # noqa

# with app.app_context():
#     if not path.exists(f"instance/{DB_NAME}"):
#         db.create_all()
#         print("Created database")
