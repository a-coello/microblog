"""Module to store web form classes.
    All imports necessary to work with web forms
    I'll need to import this classes from routes.py
    """
# To work with forms
from ast import Sub
from flask_wtf import FlaskForm
# Import the classes to create the objects in the form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
# Import this to attach validation to the fields
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
# Import User to implement user registration
from app.models import User


class LoginForm(FlaskForm):
    """LoginForm class to represent the Login form of our app
        We create the objects from the classes representing the 
        fields in this form.
        validators are used to check if the field data is correct. If not, 
        returns an error inside form.<field>.errors and we can show them
        in the html file

    Args:
        FlaskForm (class): Base class to work with forms
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """Class to implement the Registration form of our application.

    Args:
        FlaskForm (class): Base class to work with forms

    Raises:
        ValidationError: Check if the username is not in the db
        ValidationError: Check if the email is not in the db
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    # When we add any method like validate_<field_name>, WTForms takes those
    # as custom validators and invokes them is adition to the stock validators.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')  

# We build the class to manage the Edit profile form
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')