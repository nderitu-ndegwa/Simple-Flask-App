from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_session import Session
import MySQLdb.cursors
import re
import requests

app = Flask(__name__)

app.secret_key = 'FlaskApp'

# Configuring a dictionary to store user information
users_info = {}

mysql = MySQL(app)

@app.route("/")
@app.route('/login', methods =['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the user information from the form
        username = request.form['username']
        password = request.form['password']

        # Authenticate the user
        if username in users_info and users_info[username] == password:
            # Store the user information in the session
            session['user'] = {'username': username}

            return redirect(url_for('home'))
    return render_template('login.html')
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get the user information from the form
        username = request.form['username']
        password = request.form['password']

        # Store the user information in the dictionary
        users_info[username] = password

        # Store the user information in the session
        session['user'] = {'username': username}

        return redirect(url_for('login'))
    return render_template('register.html')


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