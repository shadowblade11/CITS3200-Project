from app.models import User, Question, Test


'''
This module contains a collection of functions designed to interact with a database. 
These functions have clear and meaningful names and accept specific arguments for various database operations.

The module includes functions for activating tests, writing feedback, retrieving user data, fetching tests, questions,
 and feedback, as well as setting scores for questions.

Usage:
    To use any of these functions, simply import them into your application and call them with the appropriate arguments.

Example:
    To retrieve a user's data:
    user = get_user('123')

    To set a score for a specific question:
    set_score('123', 1, 1, 95, 1)  # Sets a teacher evaluation score of 95 for question 1 in week 1 for user '123'.
'''


def activate_test(obj, week):  # Week is test_id
    students = User.get_all(is_admin=False)  # Get all the students
    if type(obj) == Test:
        for student in students:
            pass
    if type(obj) == Question:
        pass


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
    test = Test.get_all(test_id=week, user_id=user_id)  # Return a list for all the test object
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
    user = User.get(user_id)
    return user


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
    test = Test.get(user_id=user_id, test_id=week)
    return test


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
    return Question.get(user_id=user_id,test_id=week, question_id=question_num)


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


if __name__ == "__main__":
    print(1)
