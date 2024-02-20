
from __init__ import app
from db import DBConnection,insert_post
from flask import render_template, request, redirect, url_for, abort, make_response, session
import os
import uuid

@app.route('/user/<int:user_id>/', methods=['GET'])
def user_profile(user_id):
    with DBConnection() as conn:
        user_obj = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        user_bio = conn.execute("SELECT bio FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
        bio = user_bio[0]
    return render_template('user.html', user=user_obj, bio = bio)

@app.route('/')
def posts(existing_likes = False):
    if 'auth' in session and session['auth']:
        with DBConnection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM posts LEFT JOIN files ON post_id = posts.id ORDER BY id DESC')
            postes = cursor.fetchall()
        return render_template('main.html', posts=postes, existing_likes = existing_likes)
    return redirect(url_for('signup'))

@app.route('/search', methods=['POST'])
def search_user():
    username = request.form.get('username')
    with DBConnection() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user:
            return render_template('user.html', user=user, username=username)
        else:
            return render_template('main.html',username = username)






