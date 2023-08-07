from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):

    id = IntegerField('Student ID', validators=[DataRequired()])
    username = StringField('User Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    v_code = StringField('Verification Code', validators=[DataRequired()])
    send_verification = SubmitField('Send')
    passwd1 = PasswordField('Password', validators=[DataRequired()])
    passwd2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('passwd1')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    pass