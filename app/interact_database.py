from app.models import *

'''
This module contains a collection of functions designed to interact with a database. 
These functions have clear and meaningful names and accept specific arguments for various database operations.

The module includes functions for activating tests, writing feedback, retrieving user data, fetching tests, questions,
 and feedback, as well as setting scores for questions etc.

Usage:
    To use any of these functions, simply import them into your application and call them with the appropriate arguments.

Example:
    To retrieve a user's data:
    user = get_user('123')

    To set a score for a specific question:
    set_score('123', 1, 1, 95, 1)  # Sets a teacher evaluation score of 95 for question 1 in week 1 for user '123'.
'''


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