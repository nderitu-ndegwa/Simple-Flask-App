from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import requests

app = Flask(__name__)

app.secret_key = 'FlaskApp'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'FlaskApp1'
app.config['MYSQL_DB'] = 'FlaskApp'

mysql = MySQL(app)

@app.route("/")
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('index.html', msg = msg)
        else:msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)
 
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered! Please proceed to login.'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

@app.route("/home")
def home():
    return render_template("index.html")

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = '874104327a0faf91a3635ee4998adfce'
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    res = requests.get(url)
    weather_data = res.json()
    temp = weather_data['main']['temp']
    temperature = int(temp/10)
    weather_message = ""
    if temperature > 20:
        weather_message = "It's warm outside, you can do laundry today! Proceed to the calculator tab "
    else:
        weather_message = "It's cold outside, it's better to do laundry tomorrow."
    return render_template('weather.html', city=city, temperature=temperature, weather_message=weather_message)

@app.route("/Calculator")
def calculator():
    return render_template("calculator.html")

@app.route("/laundry")
def laundry():
    return render_template("laundry.html")

if __name__ == "__main__":
    app.run(debug=True)