import datetime

from flask import Blueprint
from flask import render_template, flash, redirect, url_for, abort
from flask_login import current_user, login_required
from sqlalchemy.exc import SQLAlchemyError

from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import NewPost

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=["POST", "GET"])
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
            return redirect(url_for('main.home'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while adding your post.', 'danger')
            # Логгирование ошибки или другие действия обработки ошибки

    return render_template('create_post.html', title="Create new post", form=form, legend='New Post')


@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['POST', "GET"])
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
            return redirect(url_for('main.home'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while updating your post.', 'danger')
            # Логгирование ошибки или другие действия обработки ошибки

    form.title.data = post.title
    form.content.data = post.content
    return render_template('create_post.html', title="Update post", form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    try:
        db.session.delete(post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        return redirect(url_for('main.home'))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash('An error occurred while deleting your post.', 'danger')
        # Логгирование ошибки или другие действия обработки ошибки

    return redirect(url_for('main.home'))
