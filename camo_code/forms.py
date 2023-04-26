# Imports for App
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField, FileField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileRequired
from flask_login import current_user
from camo_code.models import User, Profile, Comment, Registration, Post


# Form for Registration
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


# Form for SignIn/LogIn
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email')
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


# Form for Update Profile
class UpdateProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio')
    location = StringField('Location')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


# Form for Profile
class ProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    bio = TextAreaField('Bio')
    location = StringField('Location')
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


# Form for Posts
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    code_snippet_language = SelectField('Code Snippet Language', choices=[
        ('markup', 'Markup'), ('css', 'CSS'), ('python', 'Python'),
        ('javascript', 'JavaScript'), ('ruby', 'Ruby')])
    code_snippet = TextAreaField(
        'Code Snippet',
        render_kw={
            "class": "materialize-textarea validate",
            "data-language": "python"})
    submit = SubmitField('Update')


# Form for Comments
class CommentForm(FlaskForm):
    body = StringField('Comment', validators=[DataRequired()])
    code_snippet = TextAreaField('Code Snippet')
    code_snippet_language = SelectField('Code Snippet Language', choices=[
        ('markup', 'Markup'),
        ('css', 'CSS'),
        ('javascript', 'JavaScript'),
        ('python', 'Python'),
        ('ruby', 'Ruby')
        # add more choices for other supported languages
    ])
    submit = SubmitField('Comment')
