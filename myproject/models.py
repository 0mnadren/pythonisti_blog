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

    comments = db.relationship('Comment', backref='comment_author', lazy=True, cascade="all, delete-orphan")

    send_messages = db.relationship(
        'Message',
        backref='sender',
        foreign_keys='Message.sender_id',
        lazy=True,
        cascade="save-update")
    receive_messages = db.relationship(
        'Message',
        backref='receiver',
        foreign_keys='Message.receiver_id',
        lazy=True,
        cascade="save-update")

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


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(125), nullable=False, index=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    text = db.Column(db.Text, nullable=False, index=True)
    seen = db.Column(db.Boolean, nullable=False, default=False, index=True)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, text, sender_id, receiver_id):
        self.title = title
        self.text = text
        self.sender_id = sender_id
        self.receiver_id = receiver_id

    def __repr__(self):
        return f'Message: {self.title} -- from sender ID {self.sender_id}'





