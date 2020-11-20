from flask_wtf import Form
from wtforms import StringField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[InputRequired(),Length(min =1,max =64),Email()])
    password = PasswordField('password',validators=[InputRequired()])
    remember_me = BooleanField('keep me loggin')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Length(1, 64),Email()])
    username = StringField('Username', validators=[InputRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,'Usernames must have only letters, '
                'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[InputRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
             raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
              raise ValidationError('Username already in use.')