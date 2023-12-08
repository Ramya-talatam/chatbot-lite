from flask import Flask, render_template, request, redirect, url_for, flash, session ,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
from chatbot import getquestion, recordanswer
from journalflask import fun
app = Flask(__name__ ,static_url_path='/static')
app.secret_key = 'bluehawkhunting'

# Defining the path to the JSON file
users_file = os.path.join(os.path.dirname(__file__), 'users.json')

def read_users():
    """Read user data from the JSON file."""
    with open(users_file, 'r') as f:
        users = json.load(f)
    return users

def write_users(users):
    """Write user data to the JSON file."""
    with open(users_file, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Checking if the username already exists
        users = read_users()
        if username in users:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            # Hashing the password before storing it
            hashed_password = generate_password_hash(password, method='sha256')
            users[username] = hashed_password
            write_users(users)
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        users = read_users()

        if username in users and check_password_hash(users[username], password):
            # Successful login
            session['logged_in'] = True
            return redirect(url_for('chatbot'))
        else:
            session['message'] = 'Login failed. Please check your username and password.'
    message = session.pop('message', None)
    return render_template('login.html',message=message)

@app.route('/chatbot')
def chatbot():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('botindex.html')
@app.route('/record_answer', methods=['POST'])
def record_answer():
    answer = request.form.get('answer')
    return recordanswer(answer)
@app.route('/get_question', methods=['POST'])
def get_question():
    ques= getquestion()
    print(ques)
    return ques
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))
@app.route('/analyze', methods=['POST'])
def analyze():
    journal_text = request.form.get('journalText')
    positive_words, negative_words, focused_words,op= fun(journal_text)
    response = {
        'positive_words': positive_words,
        'negative_words': negative_words,
        'focused_words': focused_words,
        'overall_polarity': op
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run()
