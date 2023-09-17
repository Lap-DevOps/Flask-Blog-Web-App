import base64
import io
import datetime
from urllib.parse import urlsplit

from flask import Blueprint, send_file
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from flaskblog import db
from flaskblog.models import User, Post
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, UploadImageForm, Request_Reset_form, \
    Reset_Password_form
from flaskblog.users.utils import save_picture, send_reset_email



users = Blueprint('users', __name__)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query \
        .filter_by(author=user) \
        .order_by(Post.created.desc()) \
        .paginate(page=page, per_page=3)
    return render_template('user_posts.html', posts=posts, user=user)


@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, )
        db.session.add(user)
        try:
            db.session.commit()
            flash(f'Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('users.login'))
        except SQLAlchemyError as e:
            db.session.rollback()  # Откатываем транзакцию в случае ошибки
            flash(f'Error. {e}', 'danger')
            return render_template('register.html', title='Registration', form=form)

    return render_template('register.html', title='Registration', form=form)


@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        recaptcha_token = request.form.get('g-recaptcha-response')

        if user and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('You have been successfully logged in!', category='success')
            flash(f'Welcome, {user.username}!', 'success')
            next_page = request.args.get('next')
            if next_page is None or not next_page.startswith('/') or urlsplit(next_page).netloc != '':
                return redirect(url_for('main.home'))
            return redirect(next_page)
        else:
            flash('Login Unsuccessful. Invalid username or password.', category='danger')
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'danger')
    return redirect(url_for('main.home'))


@users.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm(obj=current_user)

    if form.validate_on_submit():
        try:
            form.populate_obj(current_user)
            db.session.commit()
            flash('Your profile has been updated!', 'success')
            return redirect(url_for('main.home'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while updating your profile.', 'danger')
            # Логгирование ошибки или другие действия обработки ошибки

    return render_template('account.html', title='Account', form=form)


@users.route('/user_image/<int:user_id>')
def user_image(user_id):
    user = User.query.get_or_404(user_id)
    if user.image_data:
        return send_file(io.BytesIO(user.image_data), mimetype='image/jpeg')
    else:
        return send_file('static/images/default.jpg', mimetype='image/jpeg')


@users.route('/upload_image', methods=['GET', 'POST'])
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
                return redirect(url_for('users.account'))
            except SQLAlchemyError as e:
                db.session.rollback()
                flash(f'An error occurred while updating your profile. {e}', 'danger')
                # Логгирование ошибки или другие действия обработки ошибки

    return render_template('upload_image.html', title='Account image', form=form)


@users.route('/reset_password', methods=['POST', "GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = Request_Reset_form()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent with instruction to reset your password.', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['POST', "GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid  or expired token", 'warning')
        return redirect(url_for('users.reset_request'))

    form = Reset_Password_form()

    if form.validate_on_submit():
        user.password = form.password.data

        try:
            db.session.commit()
            flash(f'Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('users.login'))
        except SQLAlchemyError as e:
            db.session.rollback()  # Откатываем транзакцию в случае ошибки
            flash(f'Error. {e}', 'danger')
            return render_template('register.html', title='Registration', form=form)
    return render_template('reset_token.html', title='Reset Password', form=form)
