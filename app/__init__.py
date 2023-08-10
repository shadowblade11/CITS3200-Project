from flask import Flask

DB_NAME = "database.db"    

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

app.app_context().push()

from app import views # imports templates for the app to use
