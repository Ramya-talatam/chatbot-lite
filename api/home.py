from flask import Flask, render_template, request, redirect, url_for, flash, session ,jsonify
# from waitress import serve
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
# from chatbot import getquestion, recordanswer
app = Flask(__name__ ,static_url_path='/static')
app.secret_key = 'bluehawkhunting'

# Defining the path to the JSON file
users_file = os.path.join(os.path.dirname(__file__), 'users.json')
from flask import Flask, render_template, request, jsonify
import re
from textblob import TextBlob as tb
message=""
q=""
intents = {
    'hi' : ['hello','hey','hi!','hi'],
    'bye' : ['goodbye','buhbye','bye'],
    'depression' : ['depressed','sad','worried','despair','misery','bad'],
    'anxiety' : ['anxiety','anxious','nervous','stress','strain','tension','discomfort','tensed'],
    'paranoia' :['disbelieve', 'distrustful', 'doubting', 'incredulous','mistrustful', 'negativistic','questioning','show-me','skeptical','suspecting','suspicious','unbelieving'],
    'sleeping_disorder' :['restlessness','indisposition','sleeplessness','stress','tension','vigil','vigilance','wakefulness'],
    'substance_abuse' :['alcohol abuse','drug abuse','drug use','addiction','alcoholic addiction','alcoholism','chemical abuse','dipsomania','drug dependence','drug habit','narcotics abuse','solvent abuse'],
    'personality_disorder':['insanity','mental disorder','schizophrenia','craziness','delusions','depression','derangement','disturbed mind','emotional disorder','emotional instability',
                            'loss of mind','lunacy','madness','maladjustment','mania','mental disease','mental sickness','nervous breakdown','nervous disorder',
                            'neurosis','neurotic disorder','paranoia','phobia','psychopathy','psychosis','sick mind','troubled mind','unbalanced mind','unsoundness of mind'],
    'happy':['good','great','relieved','happy','okay']
}

responses = {
    'hi' : 'Hello, i am a medical healthcare chatbot!',
    'bye' : 'Thank you for your time!'
}

dictionary = {
    'a':0,
    'b' : 0,
    'c' : 0,
    'd' : 0
}

s = {
    'a':0,
    'b' : 1,
    'c' : 2,
    'd' : 3
}

question = ["Do you have little interest or pleasure in doing things?","Feeling down, depressed, or hopeless","Trouble falling or staying asleep, or sleeping too much","Feeling tired or having little energy","Feeling bad about yourself - or that you are a failure or have let yourself or your family down"]


negative = 0
positive = 0

def intent(message):
    for words in intents.keys():
        pattern = re.compile('|'.join([syn for syn in intents[words]]))
        match = pattern.search(message)
        if match:
            return words
    return 'default'

def respond(message):
    word = intent(message)
    return responses[word]


def score():
    sc = 0
    for k in dictionary.keys():
        sc += dictionary[k]*s[k]
    return sc


def predict_(x):
    # tfidf = vectorizer.transform([x])
    # preds = model.predict(tfidf)
    #probab = model.predict_proba(tfidf)[0][preds]
    probab=tb(x).sentiment.polarity
    #print(preds,probab)
    feeling(probab)
    return probab

def feeling(polar):
    global negative,positive,q
    q=""
    if polar >= 0.05:
        positive +=1
        q=("That's great to hear!")
    elif polar <= -0.05:
        negative +=1
        q=("Oh, sorry to hear that!")
    else:    
        q=("Okay, thanks for sharing.")

def classification(pred):
    if pred>=0:
        return 1
    else:
        return 0

name=""
questions = ["hi",
"Hi! I'm a medical healthcare chatbot! Before we proceed, may I know your first name?",
"That's a nice name! Before we get started, I want to know about your current mood.",
"I'm a CBT coach that can consult with you during difficult times, and also not-so-difficult times. Do you wanna know a little more?",
"Mood tracking and thinking hygiene - among other useful concepts - are skills you'll learn as you practice CBT. Skills that can help you make positive changes to your thoughts, feelings and behaviour. Can you walk me through how did your last week go?",
"Can you walk me through how did your last week go?",
"I know that question can be tough and sometime painful to answer so I really appreciate you doing it... Can you tell me a bit about what's going on in your life that has brought you here today?",
"Can you tell me a bit about what's going on in your life that has brought you here today?",
"That's okay! I've listened everything you said",
"I have got great tools for people dealing with stress,wanna give it a go,Yes/No?",
"Great! Thanks for trusting me. Let's start with a small mental assessment test,so buckle up!",
"Please ask me for help whenever you feel like it! I'm always online.",
"Now we're starting with a small assessment and hopefully at the end of the assessment,we'll be able to evaluate your mental health",
"To respond please type the following answer depending upon your choice",
"A. not at all, B. several days, C. more than half a day, D. all the days. Now we'll be starting with the quiz,type okay if you're ready!",
"Do you have little interest or pleasure in doing things?",
"Feeling down, depressed, or hopeless",
"Trouble falling or staying asleep, or sleeping too much",
"Feeling tired or having little energy",
"Feeling bad about yourself - or that you are a failure or have let yourself or your family down",
"Thank you for taking the assessment!",
"Please make sure that you keep checking in with me. What's your mood now after opening up?",
"Please ask me for help whenever you feel like it! I'm always online.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! There you go...let it all slide out.Unhappiness cannot stick in a person's soul when it's slick with tear.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! Take a deep breath, listen to your thoughts, try to figure them out. Then take things one day at a time.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! If you want someone, you have to be willing to wait for them and trust that what you have is real and strong enough for them to wait for you. If somebody jumps ship for you, that fact will always haunt you because you'll know they're light on their feet. Spare yourself the paranoia and the pain and walk away until the coast is clear.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! Overhead, the glass envelope of the Insomnia Balloon is malfunctioning. It blinks on and off at arrhythmic intervals, making the world go gray:black, gray:black. In the distance, a knot of twisted trees flashes like cerebral circuitry.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! ...repeated trauma in childhood forms and deforms the personality. The child trapped in an abusive environment is faced with formidable tasks of adaptation. She must find a way to preserve a sense of trust in people who are untrustworthy, safety in a situation that is unsafe, control in a situation that is terrifyingly unpredictable, power in a situation of helplessness. Unable to care for or protect herself, she must compensate for the failures of adult care and protection with the only means at her disposal, an immature system of psychological defenses.",
"Gosh, that is tough... I am sorry to hear that. Here is a thought that might motivate you! My Recovery Must Come First So That Everything I Love In Life Doesn't Have To Come Last.",
"We're really sorry to know that and for further assistance we would try to connect you with our local assistance who is available 24/7. Here are the details -- Contact Jeevan Suicide Prevention Hotline. Address:171, Ambiga Street Golden George Nagar, Nerkundram, Chennai, Tamil Nadu 600107. Number : 044 2656 4444"
]
ans=[]
current_question = 1


def getquestion():
    global current_question
    if current_question < len(questions):
        question = q+" "+questions[current_question]
        return jsonify({'question': question})
    else:
        return jsonify({'question': 'stop'})

def recordanswer(answer):
    global current_question ,name, ans, negative, positive,q, dictionary
    q=""
    answer = request.form.get('answer')
    print(answer)
    answer= answer.lower()
    if answer=='restart':
        current_question=0
    print("prev ", current_question)
    if current_question==1:
        name=answer
    elif current_question==2:
        sentiment = predict_(answer)
    elif current_question==3 :
        sentiment=predict_(answer)
        pos=classification(sentiment)
        if pos==0:
            current_question+=1
    elif current_question in [4,5]:
        sentiment=predict_(answer)
        pos=classification(sentiment)
        if pos==1:
            current_question=6
        else:
            current_question=5
    elif current_question in [6,7]:
        sentiment = predict_(message)
        if negative != 0:
            current_question+=1
    elif current_question== 9:
        # if answer.lower()=='yes':
        if tb(answer).sentiment.polarity>=0:
            current_question=9
        else:
            current_question=10
    elif current_question == 10:
        current_question+=1
    elif current_question ==11:
        current_question = 0
    elif current_question == 14:
        if answer not in ['ok','okay']:
            current_question=0
    elif current_question in [15,16,17,18,19]:
        dictionary[answer]+=1
    elif current_question==21:
        sc=score()
        print(sc)
        if sc>=0 and sc<=13:
            m_intent=intent(answer)
            l=['happy','depression','anxiety','sleeping disorder','paranoia','personality_disorder','substance_abuse']
            if m_intent in l:
                current_question+= l.index(m_intent)
            else:
                current_question=28
        else:
            current_question=28
        
    elif current_question >=22:
        current_question=29
    current_question+=1
    print("now ", current_question )
    return jsonify({'status': 'success'})

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
    # if not session.get('logged_in'):
    #     return redirect(url_for('login'))
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
# @app.route('/analyze', methods=['POST'])
# def analyze():
#     journal_text = request.form.get('journalText')
#     positive_words, negative_words, focused_words,op= fun(journal_text)
#     response = {
#         'positive_words': positive_words,
#         'negative_words': negative_words,
#         'focused_words': focused_words,
#         'overall_polarity': op
#     }
#     return jsonify(response)

# if __name__ == '__main__':
#     # serve(app, host='127.0.0.1',port=5000, threads=4)
#     app.run()
    
