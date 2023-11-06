from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from app.database.database import Users

class SingupForm(FlaskForm):
    login = StringField('Your login (at least 3 characters long)', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Your password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up!')

    def validate_login(self, login):
        user = Users.query.filter_by(user_name=login.data).first()
        if user:
            raise ValidationError('This login is already taken. Please choose another one.')


class LoginForm(FlaskForm):
    login = StringField('Your login', validators=[DataRequired()])
    password = PasswordField('Your password', validators=[DataRequired()])
    submit = SubmitField('Log in')
