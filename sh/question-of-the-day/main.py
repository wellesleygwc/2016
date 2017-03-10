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
        age = request.form['age']
        password = request.form['password']
        if db.check_password(age, password):
            session['age'] = age
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
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

if __name__== "__main__":
    db.create_db()
    app.secret_key = os.urandom(24)
    app.run(debug=True)
