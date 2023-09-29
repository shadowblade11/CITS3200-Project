from app.models import User, Question, Test
from app import app

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
    """
        Writes feedback for a specific test.

        Args:
            user_id (str): The user ID of the student.
            feedback (str): The feedback to write.
            week (int): The week/ID of the test.

        Usage:
            write_feedback('123', 'Good job!', 1)
        """
    test = Test.get(test_id=week, user_id=user_id)  # Return a list for the test object at specific week
    test.feedback = feedback
    Test.write_to(test)


def get_user(user_id):
    """
        Retrieves user data by user ID.

        Args:
            user_id (str): The user ID of the user to retrieve.

        Returns:
            User object: The user object with the specified user ID.

        Usage:
            user = get_user('123')  # Retrieves user data for user ID '123'.
        """
    return User.get(id=user_id)


def get_test(user_id, week):
    """
        Retrieves a specific test for a user.

        Args:
            user_id (str): The user ID of the student.
            week (int): The week/ID of the test.

        Returns:
            Test object: The test object for the specified user and week.

        Usage:
            test = get_test('123', 1)  # Retrieves test for user '123' and week 1.
        """
    return Test.get(user_id=user_id, test_id=week)


def get_question(user_id, question_num, week):
    """
        Retrieves a specific question for a user and week.

        Args:
            user_id (str): The user ID of the student.
            question_num (int): The question number.
            week (int): The week/ID of the test.

        Returns:
            Question object: The question object for the specified user, week, and question number.

        Usage:
            question = get_question('123', 1, 1)  # Retrieves question 1 for user '123' in week 1.
        """
    return Question.get(user_id=user_id, test_id=week, question_id=question_num)


def get_feedback(user_id, test_id):
    """
        Retrieves feedback for a specific test.

        Args:
            user_id (str): The user ID of the student.
            test_id (int): The ID of the test.

        Returns:
            str: The feedback for the specified user and test.

        Usage:
            feedback = get_feedback('123', 1)  # Retrieves feedback for user '123' and test 1.
        """
    return Test.get(user_id=user_id, test_id=test_id).feedback


def set_score(user_id, question_id, week, score, mode):
    """
        Sets a score for a specific question.

        Args:
            user_id (str): The user ID of the student.
            question_id (int): The question number.
            week (int): The week/ID of the test.
            score (int): The score to set.
            mode (int): The scoring mode (0 for self-evaluation, 1 for teacher evaluation, 2 for program evaluation).

        Usage:
            set_score('123', 1, 1, 95, 1)  # Sets a teacher evaluation score of 95 for question 1 in week 1 for user '123'.
        """

    # Define a dictionary to map mode values to attribute names
    mode_to_attribute = {
        0: 'self_evaluation',
        1: 'teacher_evaluation',
        2: 'program_evaluation'
    }

    # Get the attribute name based on the mode
    attribute_name = mode_to_attribute.get(mode)

    if attribute_name is not None:
        # Use setattr to set the attribute value dynamically
        question = get_question(user_id, question_id, week)
        setattr(question, attribute_name, score)
        Question.write_to(question)


def set_difficulty(week, question_id, difficulty):
    questions = Question.get_all(question_id=question_id, test_id=week)
    for question in questions:
        question.difficulty = difficulty
        Question.write_to(question)


def initialize_test(week, user_id):
    test = Test(test_id=week, user_id=user_id)
    Test.write_to(test)


def admin_activate_tests(week):
    users = User.get_all()
    for user in users:
        initialize_test(week=week, user_id=user.id)


def activate_questions(question_num, week):
    tests = Test.get_all(test_id=week)
    for test in tests:
        for i in range(question_num):
            question = Question(question_id=i, test_id=week, user_id=test.user_id)
            Question.write_to(question)


if __name__ == "__main__":
    print(1)
