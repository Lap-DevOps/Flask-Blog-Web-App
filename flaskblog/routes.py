from flask import render_template, flash, redirect, url_for

from flaskblog.forms import RegistrationForm, LoginForm

from flaskblog.models import User, Post
from flaskblog import app

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Registration', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@in.ua' and form.password.data == 'admin':
            flash('You have been successfully logged in!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', category='danger')
    return render_template('login.html', title='Login', form=form)