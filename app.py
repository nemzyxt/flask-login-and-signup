# Author : Nemuel Wainaina

from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2 as psy

app = Flask(__name__)
app.secret_key = 'myV3rys3Cr3yK3yth@ty0Uc@ntgu3Ss'

def dbConnect():
    conn = psy.connect(
        database='loginsignup',
        user='postgres',
        password='_YOUR_PASSWORD_HERE_'
    )
    curs = conn.cursor()
    return conn, curs

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login/', methods=['POST', 'GET'])
def login():
    # check whether the user is already logged in and redirect to the home page
    if 'usrnm' in session:
        usrnm = session['usrnm']
        return redirect(url_for('home', usrnm=usrnm))
    if request.method == 'POST':
        usrnm = request.form['usrnm']
        passwd = request.form['passwd']
        conn, curs = dbConnect()
        q = 'SELECT * FROM users WHERE usrnm=%s AND password=%s;'
        curs.execute(q, (usrnm, passwd))
        usr = curs.fetchall()
        curs.close()
        conn.close()
        if usr:
            # success
            session['usrnm'] = usrnm # set the session variable 
            return redirect(url_for('home', usrnm=usrnm))
        else:
            # invalid creds
            msg = 'Invalid credentials, kindly try again !'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')

@app.route('/home/')
def home():
    if 'usrnm' in session:
        return render_template('home.html', usrnm=session['usrnm'])
    else:
        return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.pop('usrnm', None)
    return redirect(url_for('index'))    

@app.route('/signup/', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        usrnm = request.form['usrnm']
        email = request.form['email']
        passwd = request.form['passwd']
        conn, curs = dbConnect()
        q = 'SELECT usrnm, email FROM users;'
        curs.execute(q)
        usrs = curs.fetchall()
        if not usrs:
            # no users signed up yet, just insert the data into the table
            q = 'INSERT INTO users VALUES(%s, %s, %s);'
            curs.execute(q, (usrnm, email, passwd))
            conn.commit()
            curs.close()
            conn.close()
            return redirect(url_for('success'))
        else:
            # check whether the username or email already exists in the database
            usrnms = [usr[0] for usr in usrs]
            emails = [usr[1] for usr in usrs]
            if usrnm in usrnms:
                msg = 'Username already exists'
                return render_template('signup.html', usrnm=usrnm, email=email, passwd=passwd , usr_err=msg)
            if email in emails:
                msg = 'Email already exists'
                return render_template('signup.html', usrnm=usrnm, email=email, passwd=passwd , email_err=msg)  
            return redirect(url_for('success'))          
    else:
        return render_template('signup.html')

@app.route('/success/')
def success():
    return render_template('success.html')

if __name__ == "__main__":
    app.run(debug=True)