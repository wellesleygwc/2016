#!/usr/bin/python

# Imports
from flask import Flask, render_template, redirect, url_for, request, session
import os, sys
from app import db

app = Flask(__name__)

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.check_password(username, password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            session.clear()
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

# Home page
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    error = None
    if 'username' in session:
        username=session['username']

        return render_template('index.html', username=username, email=db.get_email(username), total_answers=db.get_total_answers(username), right_answers=db.get_right_answers(username))
    return redirect(url_for('login'))

if __name__== "__main__":
    db.create_db()
    app.secret_key = os.urandom(24)
    app.run(debug=True)
