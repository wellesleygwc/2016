#!/usr/bin/python

# Imports
from flask import Flask, render_template, redirect, url_for, request, session
import os, sys
from app import db

app = Flask(__name__)


# Home page
@app.route('/Home')
def Home():
    return render_template('HomePage.html')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.check_password(username, password):
            session['username'] = username
            return redirect(url_for('Home'))
        else:
            session.clear()
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

# Add a user
@app.route('/add user', methods=['GET', 'POST'])
def addUser():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if db.create_user(username, password, email):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            session.clear()
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)

#archives
@app.route('/archives')
def archives():
    summary = db.question_summary()
    print summary
    return render_template('Archives.html', summary=summary)

#Question
@app.route('/question')
def question():
    id = request.args.get('id')
    question = db.get_question(id)
    return render_template('Question.html',question=question)

# Login page
@app.route('/')
@app.route('/logins', methods=['GET', 'POST'])
def logins():
    error = None
    if 'username' in session:
        username=session['username']
        return render_template('Profile.html', username=username, email=db.get_email(username), total_answers=db.get_total_answers(username), right_answers=db.get_right_answers(username))
    return redirect(url_for('login'))

#Profile
@app.route('/Profile')
def profile():
    return render_template('Profile.html')


if __name__== "__main__":
    db.create_db()
    app.secret_key = os.urandom(24)
    app.run(debug=True)
