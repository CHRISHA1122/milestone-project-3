from camo_code import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_wtf import FlaskForm
from flask_login import UserMixin
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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
    language = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(140))
    body = db.Column(db.String(280))
    code_snippet = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comments = db.relationship("Comment", backref="post", lazy="dynamic")

    def __repr__(self):
        return "<Post {}>".format(self.title)

    def update(self, title, body, code_snippet):
        self.title = title
        self.body = body
        self.code_snippet = code_snippet
        db.session.commit()

    def formatted_code_snippet(self):
        return Markup(f'<pre><code class="language-{self.language}">{self.code_snippet}</code></pre>')

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Comment(db.Model):
    # schema for the Comment model
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    code_snippet = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post_relationship = db.relationship(
        'Post', backref=db.backref('post_comments', lazy=True))

    def __repr__(self):
        return f"Comment('{self.body}', '{self.date_posted}')"

    def delete(self):
        db.session.delete(self)
        db.session.commit()


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
