from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from flask_wtf import FlaskForm

from wtforms.validators import ValidationError


def is_integer(form, field):
    if not field.data.isdigit():
        raise ValidationError('Input must be an integer')


class RegistrationForm(FlaskForm):
    id = StringField('Student ID', validators=[DataRequired(message="Please enter your student ID"), is_integer])
    v_code = StringField('Verification Code', validators=[DataRequired(message="Please enter the verification code "
                                                                               "you received")])
    send_verification = SubmitField('Send')
    passwd1 = PasswordField('Password', validators=[DataRequired(message="Please enter your password")])
    passwd2 = PasswordField('Repeat Password', validators=[DataRequired(message="Repeat your password"),
                                                           EqualTo('passwd1', message="Password must match")])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    id = StringField('Student ID', validators=[DataRequired(message="Please enter your student ID"),is_integer])
    passwd = PasswordField('Password', validators=[DataRequired(message="Please enter your password")])
    submit = SubmitField('Sign In')
    register = SubmitField('Do not have a account? Click here to register!')
