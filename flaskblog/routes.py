from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, logout_user,login_required
from sqlalchemy.exc import IntegrityError

from flaskblog import app, db
from flaskblog.forms import RegistrationForm, LoginForm
from .models import User

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', posts=posts)


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
        except IntegrityError as e:
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


@app.route('/account')
@login_required
def account():
    user = current_user
    return render_template('account.html', title='Account')