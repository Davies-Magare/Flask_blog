#!/usr/bin/python3
from . import db

class User(db.Model):
    """User class representing a user in the blog application"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(650), nullable=False)
    posts = db.relationship('Post', back_populates='user')

class Post(db.Model):
    """Post class representing a post in the blog application"""
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.String(500), nullable=False)
    user = db.relationship('User', back_populates='posts')
