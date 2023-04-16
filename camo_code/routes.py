from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from camo_code import app, db
from camo_code.models import User, Post, Comment
from camo_code.forms import LoginForm, RegistrationForm, UpdateProfileForm, PostForm


@app.route("/")
def home():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template("home.html", posts=posts)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", current_user=current_user)


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
        return redirect(url_for("login"))
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
        post = Post(
            title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!")
        return redirect(url_for("home"))
    return render_template("new_post.html", title="New Post", form=form)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data, post=post, author=current_user)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been added!")
        return redirect(url_for("post", post_id=post.id))
    return render_template("post.html", post=post, form=form)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        flash("You do not have permission to update this post.")
        return redirect(url_for("post", post_id=post.id))
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data

        # get the code associated with the post
        code = post.codes.first()

        # update the code information
        code.title = form.code_title.data
        code.body = form.code_body.data
        code.language = form.language.data

        db.session.commit()
        flash("Your post has been updated!")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.body.data = post.body

        # pre-populate form fields with existing code data
        code = post.codes.first()
        form.code_title.data = code.title
        form.code_body.data = code.body
        form.language.data = code.language

    return render_template("new_post.html", title="Update Post", form=form)


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
