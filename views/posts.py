from __init__ import app
from db import DBConnection, insert_post
from flask import render_template, request, redirect, url_for, abort, make_response, session
import os
import uuid


@app.route('/postCreate')
def render_post_create():
    if session['login'] == 'admin':
        return render_template('postCreate.html')
    return redirect(url_for('posts'))


@app.route('/post/<int:post_id>')
def render_post(post_id):
    filename = None
    with DBConnection() as conn:
        post = (conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone())
        post_name = post[1]
        content = post[2]
        file = conn.execute('SELECT music FROM files where post_id = ?', (post_id,)).fetchone()
        if file:
            filename = file[0]
        print(post_name, ' ', content, ' ')
    return render_template('post.html', post_name=post_name, content=content, filename=filename)


@app.route('/post_creat', methods=['POST'])
def post_create():
    name = request.form.get('name')
    content = request.form.get('content')
    username = session.get('username')
    music = request.files['music_uploading']
    filename = ''
    if music:
        filename = str(uuid.uuid4()) + '.mp3'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        music.save(filepath)
        print(filename)

    with DBConnection() as conn:
        user_id = session['user_id']
        print(user_id)
        conn.execute('INSERT INTO posts (post_name, content,user_id ) VALUES (?, ?, ?)', (name, content, user_id))
        post_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
        if music:
            conn.execute('INSERT INTO files(post_id, music) VALUES (?, ?)', (post_id, filename,))
            print(filename)
        # return redirect('post.html', post_name=name, content=content, filename= filename,user_id=user_id)
        return redirect(url_for('render_post', post_id=post_id))


@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    user_id = session['user_id']
    existing_likes = {}

    with DBConnection() as conn:
        existing_like = conn.execute("SELECT * FROM likes WHERE user_id = ? AND post_id = ?",
                                     (user_id, post_id)).fetchone()
        if not existing_like:
            existing_like = True
            conn.execute('UPDATE posts SET likes_count = likes_count + 1 WHERE id = ?', (post_id,))
            conn.execute('INSERT INTO likes (post_id, user_id) VALUES (?, ?)', (post_id, session['user_id']))
            existing_likes[post_id] = True

    return redirect(url_for('posts', existing_likes=existing_likes))


def unlike_post(post_id):
    user_id = session['user_id']
    existing_likes = {}

    with DBConnection() as conn:
        existing_like = conn.execute("SELECT * FROM likes WHERE user_id = ? AND post_id = ?",
                                     (user_id, post_id)).fetchone()
        if existing_like:
            existing_like = True
            conn.execute("DELETE FROM likes WHERE user_id = ? AND post_id = ?", (user_id, post_id))
            conn.execute('UPDATE posts SET likes_count = likes_count - 1 WHERE id = ?', (post_id,))
            existing_likes[post_id] = False  # Устанавливаем состояние отсутствия лайка для данного поста

    return redirect(url_for('posts', existing_likes=existing_likes))


@app.route('/viewlike/<int:post_id>', methods=['GET', 'POST'])
def view_likes(post_id):
    with DBConnection() as conn:
        likes = conn.execute(
            'SELECT users.id, users.username FROM likes JOIN users ON likes.user_id = users.id WHERE likes.post_id = ?',
            (post_id,)).fetchall()

    return render_template('viewlikes.html', likes=likes)
