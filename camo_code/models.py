from camo_code import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
import psycopg2


class User(db.Model, UserMixin):
    # schema for the User model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Profile(db.Model):
    # schema for the Profile model
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    bio = db.Column(db.String(280))
    location = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Profile {}>".format(self.first_name)

    def delete_profile(self):
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    # schema for the Post model
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    body = db.Column(db.String(280))
    code_snippet = db.Column(db.Text)
    code_snippet_language = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))
    comments = db.relationship("Comment", backref="post", lazy="dynamic")

    def __repr__(self):
        return "<Post {}>".format(self.title)

    def update(self, title, body, code_snippet, code_snippet_language):
        self.title = title
        self.body = body
        self.code_snippet = code_snippet
        self.code_snippet_language = code_snippet_language

    def formatted_code_snippet(self):
        return Markup(f'<pre><code class="language-{self.code_snippet_language}">{self.code_snippet}</code></pre>')

    def add_comment(self, body, code_snippet):
        comment = Comment(body=body, code_snippet=code_snippet, post=self)
        db.session.add(comment)
        db.session.commit()

    def delete(self, user):
        if self.user_id == user.id:
            db.session.delete(self)
            db.session.commit()


class Comment(db.Model):
    # schema for the Comment model
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    code_snippet = db.Column(db.Text)
    code_snippet_language = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"))

    def __repr__(self):
        return f"Comment('{self.body}', '{self.date_posted}')"

    def delete(self, user):
        if self.user_id == user.id:
            db.session.delete(self)
            db.session.commit()


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


class Registration(db.Model):
    # schema for the Registration model
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<Registration {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class RegistrationForm(FlaskForm):
    # schema for the registrationform model
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def save(self):
        existing_user = Registration.query.filter_by(
            username=self.username.data).first()
        if existing_user:
            flash('A user with that username already exists.')
        return False

        existing_email = Registration.query.filter_by(
            email=self.email.data).first()
        if existing_email:
            flash('A user with that email already exists.')
        return False

        registration = Registration(
            username=self.username.data, email=self.email.data)
        registration.set_password(self.password.data)
        db.session.add(registration)
        db.session.commit()

        login_user(registration)

        return redirect(url_for('profile'))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
