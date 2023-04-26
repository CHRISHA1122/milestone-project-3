from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from camo_code import app, db
from camo_code.models import User, Post, Comment, Profile
from camo_code.forms import LoginForm, RegistrationForm, UpdateProfileForm
from camo_code.forms import ProfileForm, PostForm, CommentForm
from datetime import datetime
import logging
from pprint import pprint


@app.route("/")
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("home.html", posts=posts)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", current_user=current_user)


@app.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        if current_user.profile:
            current_user.profile.first_name = form.first_name.data
            current_user.profile.last_name = form.last_name.data
            current_user.username = form.username.data
            current_user.email = form.email.data
            current_user.profile.bio = form.bio.data
            current_user.profile.location = form.location.data
        else:
            profile = Profile(first_name=form.first_name.data,
                              last_name=form.last_name.data,
                              user_id=current_user.id,
                              bio=form.bio.data,
                              location=form.location.data)
            current_user.username = form.username.data
            db.session.add(profile)
        db.session.commit()
        flash("Your profile has been updated!")
        return redirect(url_for("profile", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        profile = Profile.query.filter_by(user_id=current_user.id).first()
        if profile:
            form.first_name.data = profile.first_name
            form.last_name.data = profile.last_name
            form.email.data = current_user.email
            form.bio.data = profile.bio
            form.location.data = profile.location
    return render_template(
        "update_profile.html", title="Update Profile", form=form)


@app.route("/delete_profile", methods=["POST"])
@login_required
def delete_profile():
    if current_user.profile:
        db.session.delete(current_user.profile)
        db.session.commit()
    logout_user()
    flash('Your profile has been deleted.')
    return redirect(url_for('home'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("home"))
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = UpdateProfileForm()
    if form.validate_on_submit():
        user.username = form.username.data
        db.session.commit()
        flash("Your profile has been updated.")
        return redirect(url_for("user", username=user.username))
    elif request.method == "GET":
        form.username.data = user.username
        form.about_me.data = user.about_me
    return render_template("user.html", user=user, form=form)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(code_snippet_language=form.code_snippet_language.data,
                    title=form.title.data,
                    body=form.body.data,
                    code_snippet=form.code_snippet.data,
                    timestamp=datetime.utcnow(),
                    user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!")
        return redirect(url_for("home"))
    return render_template("new_post.html", form=form)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, user=current_user)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added!")
        return redirect(url_for("post", post_id=post.id))
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template(
        "post.html", title=post.title, post=post, form=form, comments=comments)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.code_snippet = form.code_snippet.data
        code_snippet_language = form.code_snippet_language.data
        db.session.commit()
        flash("Your post has been updated!")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.body.data = post.body
        form.code_snippet.data = post.code_snippet or ''
        form.code_snippet_language.data = post.code_snippet_language

    return render_template(
        "update_post.html", title="Update Post", post=post, form=form)


@app.route("/post/<int:post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("You do not have permission to delete this post.")
        return redirect(url_for("post", post_id=post.id))
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted.")
    return redirect(url_for("home"))


@app.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
@login_required
def comment(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          code_snippet_language=form.code_snippet_language.data
                          )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been added.')
        return redirect(url_for('post', post_id=post_id))
    return render_template('comment.html', title='Add Comment', form=form, post=post)
