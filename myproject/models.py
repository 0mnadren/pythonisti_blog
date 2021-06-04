from myproject import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(255), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False, index=True)

    posts = db.relationship('Blog', backref='author', lazy=True, cascade="all, delete-orphan")

    comments = db.relationship('Comment', backref='author', lazy=True, cascade="all, delete-orphan")

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'Username {self.username} -- {self.email}'


class Blog(db.Model):
    __tablename__ = 'blogs'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    title = db.Column(db.String(125), nullable=False, index=True)
    text = db.Column(db.Text, nullable=False, index=True)

    comments = db.relationship('Comment', backref='blog', lazy=True, cascade="all, delete-orphan")

    users = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f'Post ID: {self.id} -- Date: {self.date} -- {self.title}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    text = db.Column(db.Text, nullable=False, index=True)

    users = db.relationship(User)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    blogs = db.relationship(Blog)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

    def __init__(self, text, user_id, blog_id):
        self.text = text
        self.user_id = user_id
        self.blog_id = blog_id

    def __repr__(self):
        return f'Comment ID: {self.id} -- Blog ID: {self.blog_id} -- User ID {self.user_id}'



