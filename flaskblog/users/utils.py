import base64
import datetime
import io
import os
import secrets
from threading import Thread

from PIL import Image
from flask import render_template, flash, redirect, url_for, send_file, current_app
from flask_login import current_user, login_required
from flask_mail import Message
from sqlalchemy.exc import SQLAlchemyError

from flaskblog import app, db, mail
from models import User
from users.forms import UploadImageForm, Request_Reset_form, Reset_Password_form





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


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_reset_email(user, sync=False):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", recipients=[user.email])
    msg.body = render_template('reset_password.txt', user=user, token=token)
    msg.html = render_template('reset_password.html', user=user, token=token)

    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
               args=(current_app._get_current_object(), msg)).start()


@app.route('/reset_password', methods=['POST', "GET"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = Request_Reset_form()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Email has been sent with instruction to reset your password.', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['POST', "GET"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid  or expired token", 'warning')
        return redirect(url_for('reset_request'))

    form = Reset_Password_form()

    if form.validate_on_submit():
        user.password = form.password.data

        try:
            db.session.commit()
            flash(f'Your password has been updated! You are now able to log in', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            db.session.rollback()  # Откатываем транзакцию в случае ошибки
            flash(f'Error. {e}', 'danger')
            return render_template('register.html', title='Registration', form=form)
    return render_template('reset_token.html', title='Reset Password', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    image = Image.open(form_picture)
    new_size = (150, 150)
    image.thumbnail(new_size)
    image.save(picture_path)
