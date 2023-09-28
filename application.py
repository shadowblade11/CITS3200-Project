from app import app, db, interact_database
from app.models import User, Test, Question

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'User': User,
        'Test': Test,
        'Question': Question,
        'write_feedback': interact_database.write_feedback,
        'get_user': interact_database.get_user,
        'get_test': interact_database.get_test,
        'get_question': interact_database.get_question,
        'get_feedback': interact_database.get_feedback,
        'set_score': interact_database.set_score,
        'set_difficulty': interact_database.set_difficulty,
        'initialize_test': interact_database.initialize_test,
    }


app.app_context().push()
app.static_folder = 'app/static'
