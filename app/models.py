from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    privilege = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index=True)
    email = db.Column(db.String(120), index=True)
    message = db.Column(db.String(200))

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(64))
    text = db.Column(db.String(1024))
    #should be changed to datetime.utcnow in case of multiple time zones
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    comments = db.relationship('BlogPostComment', backref='post', lazy='dynamic')


class BlogPostComment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), index=True)
    comment = db.Column(db.String(128), index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    post_id = db.Column(db.Integer, db.ForeignKey('blog_post.id'))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
