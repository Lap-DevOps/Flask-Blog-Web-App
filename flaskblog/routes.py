import base64
import datetime
import io
import os
import secrets

from PIL import Image
from flask import render_template, flash, redirect, url_for, request, send_file, abort
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from flaskblog import app, db
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, UploadImageForm, NewPost
from .models import User, Post


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    image = Image.open(form_picture)
    new_size = (150, 150)
    image.thumbnail(new_size)
    image.save(picture_path)


@app.route("/")
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)


@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query\
        .filter_by(author=user)\
        .order_by(Post.created.desc())\
        .paginate(page=page, per_page=1)
    return render_template('user_posts.html', posts=posts, user=user)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, )
        db.session.add(user)
        try:
            db.session.commit()
            flash(f'Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            db.session.rollback()  # Откатываем транзакцию в случае ошибки
            flash(f'Error. {e}', 'danger')
            return render_template('register.html', title='Registration', form=form)

    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You have been successfully logged in!', category='success')
            flash(f'Welcome, {user.username}!', 'success')
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/'):
                return redirect(url_for('home'))
            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Invalid username or password.', category='danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect('home')


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm(obj=current_user)

    if form.validate_on_submit():
        try:
            form.populate_obj(current_user)
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('home'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.', 'danger')
            # Логгирование ошибки или другие действия обработки ошибки

    return render_template('account.html', title='Account', form=form)


@app.route('/user_image/<int:user_id>')
def user_image(user_id):
    user = User.query.get_or_404(user_id)
    if user.image_data:
        return send_file(io.BytesIO(user.image_data), mimetype='image/jpeg')
    else:
        return send_file('static/images/default.jpg', mimetype='image/jpeg')


@app.route('/upload_image', methods=['GET', 'POST'])
@login_required
def upload_image():
    form = UploadImageForm(obj=current_user)

    if form.validate_on_submit():
        if form.image.data.filename:
            image = form.image.data
            user = current_user

            image_data_base64 = base64.b64decode(form.binary_data.data.split(',')[1])
            user.image_data = image_data_base64

            user.image_filename = image.filename
            user.image_mimetype = image.mimetype
            user.uploaded = datetime.datetime.utcnow()
            save_picture(form.image.data)
            try:
                form.populate_obj(current_user)
                db.session.commit()
                flash('Image uploaded successfully!', 'success')
                return redirect(url_for('account'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'An error occurred while updating your profile. {e}', 'danger')
                # Логгирование ошибки или другие действия обработки ошибки

    return render_template('upload_image.html', title='Account image', form=form)


@app.route("/post/new", methods=["POST", "GET"])
@login_required
def new_post():
    form = NewPost()

    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data,
                    author=current_user,
                    created=datetime.datetime.utcnow())

        try:
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect(url_for('home'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while adding your post.', 'danger')
            # Логгирование ошибки или другие действия обработки ошибки

    return render_template('create_post.html', title="Create new post", form=form, legend='New Post')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['POST', "GET"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = NewPost()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.created = datetime.datetime.utcnow()
        try:
            db.session.add(post)
            db.session.commit()
            flash('Your post has been updated!', 'success')
            return redirect(url_for('home'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while updating your post.', 'danger')
            # Логгирование ошибки или другие действия обработки ошибки

    form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html', title="Update post", form=form, legend='Update Post')


@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    try:
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('home'))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('An error occurred while deleting your post.', 'danger')
        # Логгирование ошибки или другие действия обработки ошибки

    return redirect(url_for('home'))
