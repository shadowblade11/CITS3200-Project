from app.models import *


def write_feedback(user_id, feedback, week):
    test = Test.get(week_number=week)
    if test is None:
        raise ValueError(f"Test for week {week} doesn't exist!")
    fb = Feedback.get(user=user_id, week=week)
    fb.set_feedback(feedback)
    Feedback.write_to(fb)


def initialize_test(week, name, due, quantity):  # After initialize the test the users' complete and feedback will be created
    '''
    Invoke to activate a test, create relevant tables for all the students.
    :param week: week number
    :param name: the name of the test
    :param due: the due day of the test
    :param quantity: the number of questions
    :return: None
    '''

    test = Test(week_no=week, test_name=name, due_date=due, no_of_qs=quantity)
    Test.write_to(test)

    users = User.get_all()
    for user in users:  # Initialize feedback and complete table for all users in this week
        completed = Complete(user=user.username, week=week)
        feedback = Feedback(user=user.username, week=week)
        Complete.write_to(completed)
        Feedback.write_to(feedback)


def admin_activate_tests(week, questions):
    """
    Invoke whenever a test is initialized by an admin user, and admin has already uploaded the questions for this week.
    questions is a list of tuples[('q1', 6), ('q2', 3)..., ('qn', 9)]
    The first element in the tuple is the question name and the second element in the tuple is the difficulty.
    """
    test = Test.get(week_number=week)

    if test is None:
        raise ValueError(f"Test for week {week} doesn't exist!")

    if len(questions) != test.number_of_questions:
        raise ValueError("The number of provided questions doesn't match the expected number for this test.")
    number_of_questions = test.number_of_questions

    for i in range(number_of_questions):
        q = Question(question_name=questions[i][0], difficulty=questions[i][1], test_id=test.week_number)
        Question.write_to(q)


def set_score(score, username, week, question_name, type):
    test = Test.get(week_number=week)
    question = Question.get(question_name=question_name)
    if test is None:
        raise ValueError(f"Test for week {week} doesn't exist!")
    if question is None:
        raise ValueError(f"Question {question_name} doesn't exist!")

    scores = Score(user=username, week=week, question_name=question_name)

    if type == 'self':
        scores.user_score = score
    elif type == 'program':
        scores.sys_score = score
    else:
        raise ValueError("No such type of score.")

    Score.write_to(scores)