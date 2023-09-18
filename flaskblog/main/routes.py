from flask import Blueprint
from flask import render_template, request

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