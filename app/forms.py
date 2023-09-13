from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from flask_wtf import FlaskForm


def check_id(form, field):
    if not field.data.isdigit():
        raise ValidationError('Input must be an integer')
    if not len(field.data) == 8:
        raise ValidationError('Student ID is 8 digit')


def check_password_strength(form, field):  # TODO: add to form later on
    password = field.data
    # Implement your password strength requirements here
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")
    if not any(c.isdigit() for c in password):
        raise ValidationError("Password must contain at least one digit")
    if not any(c.isalpha() for c in password):
        raise ValidationError("Password must contain at least one letter")


class RegistrationForm(FlaskForm):
    id = StringField('Student ID', validators=[DataRequired(message="Please enter your student ID")])
    passwd1 = PasswordField('Password', validators=[DataRequired(message="Please enter your password")])
    passwd2 = PasswordField('Repeat Password', validators=[DataRequired(message="Repeat your password"),
                                                           EqualTo('passwd1', message="Password must match")])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    id = StringField('Student ID', validators=[DataRequired(message="Please enter your student ID")])
    passwd = PasswordField('Password', validators=[DataRequired(message="Please enter your password")])
    submit = SubmitField('Sign In')


class VerificationForm(FlaskForm):
    # id = StringField('Student ID', validators=[DataRequired(message="Please enter your student ID"), check_id])
    v_code = StringField('Verification Code')
    send_verification = SubmitField('Check')


class AdminForm(FlaskForm):
    username = StringField('Admin Email', validators=[DataRequired(message="Please enter your Admin email")])
    passwd = PasswordField('Password', validators=[DataRequired(message="Please enter your password")])
    submit = SubmitField('Sign In')
    # marinella.caruso@uwa.edu.au

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')
