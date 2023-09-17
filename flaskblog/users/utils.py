import os
import os
import secrets
from threading import Thread

from PIL import Image
from flask import render_template, current_app
from flask_mail import Message

from flaskblog import mail


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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    image = Image.open(form_picture)
    new_size = (150, 150)
    image.thumbnail(new_size)
    image.save(picture_path)
