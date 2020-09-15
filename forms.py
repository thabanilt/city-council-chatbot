from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,TextAreaField,RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,InputRequired
from flask_wtf.file import FileField, FileAllowed,FileRequired


class RegistrationForm(FlaskForm):
    
    name = StringField('Fullname',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    # gender = RadioField('Gender',choices = [('Male','Male'),('Female','Female')], validators=[InputRequired()])

    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    # address = TextAreaField('Home Address',  validators=[DataRequired(), Length(min=2, max=100)])
    # picture = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png']),FileRequired()])

    submit = SubmitField('Sign Up')

 

    # def validate_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('That email is taken. Please choose a different one.')
class Schedule(FlaskForm):
    day = StringField('Enter Day',
                           validators=[DataRequired(), Length(min=2, max=20)])
    areas = StringField('Pick Up Areas',
                           validators=[DataRequired(), Length(min=2, max=20)])
    duration = StringField('Duration',
                           validators=[DataRequired(), Length(min=2, max=20)])



class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
