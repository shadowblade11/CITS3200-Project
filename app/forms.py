from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from flask_wtf import FlaskForm



def check_id(form, field):
    if not field.data.isdigit():
        raise ValidationError('Input must be an integer')
    if not len(field.data) == 8:
        raise ValidationError('Student ID is 8 digit')


class RegistrationForm(FlaskForm):
    id = StringField('Student ID', validators=[DataRequired(message="Please enter your student ID"), check_id])
    passwd1 = PasswordField('Password', validators=[DataRequired(message="Please enter your password")])
    passwd2 = PasswordField('Repeat Password', validators=[DataRequired(message="Repeat your password"),
                                                           EqualTo('passwd1', message="Password must match")])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    id = StringField('Student ID', validators=[DataRequired(message="Please enter your student ID"),check_id])
    passwd = PasswordField('Password', validators=[DataRequired(message="Please enter your password")])
    submit = SubmitField('Sign In')


class VerificationForm(FlaskForm):
    # id = StringField('Student ID', validators=[DataRequired(message="Please enter your student ID"), check_id])
    v_code = StringField('Verification Code')
    send_verification = SubmitField('Send')
