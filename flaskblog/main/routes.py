import os

from flask import Blueprint, send_from_directory
from flask import render_template, request,current_app

from flaskblog.models import Post

main = Blueprint('main', __name__, static_folder='static', template_folder='templates')


@main.route("/")
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts)


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(current_app.root_path, 'static', 'images'),
                               'flask_icon.png', mimetype='image/png')

