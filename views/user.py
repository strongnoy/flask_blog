from __init__ import app, session
from db import DBConnection
from flask import render_template, request, redirect, url_for, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import os
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if session.get('auth'):
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form.get('username').lower()
        password = request.form.get('password')
        print(username, password)
        if not username:
            return "Username is required"
        if not password:
            return "Password is required"

        with DBConnection() as conn:
            exist_username = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if exist_username:
                return "Username already exists"

            password = generate_password_hash(password)
            conn.execute("INSERT INTO users (username, password) values (?, ?)", (username, password))
            user_id = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()[0]
            conn.execute("INSERT INTO profiles (user_id, full_name) values (?, ?)", (user_id, username))
            session['auth'] = True
            session['login'] = username
            session['user_id'] = user_id
            session['counter'] = 0

            return redirect(url_for('profile'))

    return render_template('signup.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('auth'):
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form.get('username').lower()
        password = request.form.get('password')
        with DBConnection() as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
            if not user or not check_password_hash(user['password'], password):
                return "Invalid"

        session['auth'] = True
        session['login'] = username
        session['user_id'] = user['id']
        session['counter'] = session.get('counter', 0)

        return redirect(url_for('profile'))

    return render_template('signin.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signup'))

@app.route('/profile')
def profile():
    if 'auth' in session and session['auth']:
        with DBConnection() as conn:
            description = conn.execute("SELECT bio FROM profiles WHERE user_id = ?", (session['user_id'],)).fetchone()
            if description:
                bio = description[0]
                return render_template('profile.html', bio = bio)
            return render_template('profile.html')
    return redirect(url_for('login'))
@app.route('/update_bio', methods=['GET', 'POST'])
def update_bio():
    if 'auth' not in session or not session['auth']:
        return redirect(url_for('signup'))
    if request.method == 'POST':
        new_description = request.form.get('bio')
        with DBConnection() as conn:
            cursor = conn.cursor()
            user_id = session['user_id']
            cursor.execute("UPDATE profiles SET bio = ? WHERE user_id = ?", (new_description, user_id,))

            conn.commit()
        return redirect(url_for('profile'))
@app.route('/delete_profile', methods = ['POST'])
def delete_profile():
    user_id = session['user_id']
    with DBConnection() as conn:
        conn.execute('DELETE FROM USERS WHERE ID = ?', (user_id,))

    session.clear()

    return redirect(url_for('signup'))



