from app import app, db
from app.models import User, Test, Question
from app.interact_database import *


@app.shell_context_processor
def make_shell_context():
    return globals()


app.app_context().push()
app.static_folder = 'app/static'
