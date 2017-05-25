#!/usr/bin/python

# Imports
from flask import Flask, render_template, redirect, url_for, request, session
import os, sys
from app import db

app = Flask(__name__)


# Home page
@app.route('/home')
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
    return render_template('Archives.html', summary=summary)

#Question
@app.route('/question')
def question():
    id = request.args.get('id')
    question = db.get_question(id)
    return render_template('Question.html', question=question, answers=db.get_question_answers(id))

#Answers
@app.route('/answers', methods=['GET', 'POST'])
def answers(href=None):
    correct = request.form['answer']
    id = 0
    if correct == 'w':
        id = str('Your answer is wrong.')
    elif correct == 'r':
        id = str('Your answer is correct! Good job!')
    return render_template('answers.html', id=id)

# Login page
@app.route('/')
@app.route('/logins', methods=['GET', 'POST'])
def logins():
    if 'username' in session:
        username=session['username']
        return render_template('Profile.html', username=username, email=db.get_email(username), total_answers=db.get_total_answers(username), right_answers=db.get_right_answers(username))
    return redirect(url_for('login'))


# Logout page
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
         del session['username']
    return render_template('logout.html')

#Profile
@app.route('/profile')
def profile():
    return render_template('Profile.html')

@app.route('/change password', methods=['GET', 'POST'])
def change_password():
    new_password=request.form['new_password']
    confirm_password=request.form['confirm_password']
    if new_password!=confirm_password:
        return render_template('Profile.html', error_message="passwords don't match")
    username=session['username']
    old_password=request.form['new_password']
    status = db.change_password(username, old_password, new_password)
    return render_template('Profile.html', error_message=status)



if __name__== "__main__":
    db.create_db()
    app.secret_key = os.urandom(24)
    app.run(debug=True)
