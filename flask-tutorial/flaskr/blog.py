from flask import (
        Blueprint, flash, g, redirect, render_template, request, url_for
    )
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from .db import db
from sqlalchemy import text
from .models import Post

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    #Home page to display all posts
    query = text('''
    SELECT p.id, p.title, p.body, p.created, u.username
    FROM post p
    JOIN user u ON p.author_id = u.id
    ORDER BY p.created DESC
''')
    posts = db.session.execute(query).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            new_post = Post(title=title, body=body, author_id=g.user.id)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('blog/create.html')

def get_post(id, check_author=True):
    """Retrieve a post from the database."""
    query = text('''
    SELECT p.id, title, body, created, author_id, username
    FROM post p JOIN user u ON p.author_id = u.id
    WHERE p.id = :id
    ''')
    id_dict = {'id': id}
    post = db.session.execute(query, **id_dict).fetchone()
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    if check_author and post['author_id'] != g.user['id']:
        abort(403)
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if post:
        print(yes)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            query_parameters = {'title': title, 'body':body, 'id':id}
            query = text('''
            UPDATE post SET title = :title, body = :body
            WHERE id = :id
            ''')
            db.session.execute(query, **query_parameters)
            db.session.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    id_parameter = {'id': id}
    query = text('''
    DELETE FROM post WHERE id = :id
    ''')
    db.session.execute(query, **id_parameter)
    db.session.commit()
    return redirect(url_for('blog.index'))

