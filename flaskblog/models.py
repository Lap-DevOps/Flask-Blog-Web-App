import re
from datetime import datetime

from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin

from flaskblog import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User Authentication fields
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120, collation='NOCASE'), unique=True, nullable=False)
    # email_confirmed_at = db.Column(db.DateTime(), default=False)
    # confirmed = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))

    # User fields
    # first_name = db.Column(db.String(50), nullable=False)
    # last_name = db.Column(db.String(50), nullable=False)
    # image_file = db.Column(db.LargeBinary)
    # member_since = db.Column(db.DateTime(), default=datetime.utcnow())  # we will use moments.js af
    # last_seen = db.Column(db.DateTime(), default=datetime.utcnow())

    # roles = db.relationship('Role',
    #                         secondary='user_roles',
    #                         backref='person',
    #                         lazy='dynamic')

    posts = db.relationship('Post',
                            backref='author',
                            lazy='dynamic',
                            cascade='all, delete-orphan')
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User :  {self.username}, email: {self.email}, ID: {self.id}>'


# Define the Role data-model
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), unique=True)
#     description = db.Column(db.String(255))
#     default = db.Column(db.Boolean, default=False, index=True)
#     permissions = db.Column(db.Integer)
#
#     def __repr__(self):
#         return '<Role %r>' % self.name


# Define the UserRoles association table
# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


def slugify(s):
    pattern = r'[^\w+]'
    return re.sub(pattern, '-', s)


class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    title = db.Column(db.String(140), nullable=False)
    # slug = db.Column(db.String(140), unique=True)
    content = db.Column(db.Text, nullable=False)
    # created = db.Column(db.DateTime(), index=True, default=datetime.now)
    # views = db.Column(db.Integer, default=0)
    # likes = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            self.slug = slugify(self.title)

    def __repr__(self):
        return f"<Post id: {self.id}, title: {self.title}>"
