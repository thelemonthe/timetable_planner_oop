from flask import Flask, render_template, request, redirect, url_for, session, flash, g   
from flask_sqlalchemy import SQLAlchemy
import sqlite3 
import time 
import datetime

password_legible_check = False
session_id = 0
app = Flask(__name__)
app.secret_key = "no_guts_no_glory"

#connection = sqlite3.connect('timetable_database.db')  
connection = sqlite3.connect('database_prototype.db', check_same_thread=False)                                                                       
cursor = connection.cursor()

try:
    cursor.execute("""CREATE TABLE accounts (
    account_id INTEGER PRIMARY KEY,
    username TEXT,
    email TEXT,
    password TEXT,
    account_date_of_creation DATETIME,
    account_status TEXT
    )
    """)
except:
    useless_variable = "I'm a useless variable! "
    
try:
    cursor.execute("""CREATE TABLE commitments (
    commitment_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    commitment_datetime DATETIME,
    commitment_description TEXT,
    commitment_date_of_creation INTEGER,
    commitment_name TEXT
    )
    """)
except:
    useless_variable = "I'm a useless variable! "

try:
    cursor.execute("""CREATE TABLE events (
    event_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    event_datetime DATETIME,
    event_description TEXT,
    event_date_of_creation DATETIME,
    event_repeat TEXT,
    event_name TEXT
    )
    """)
except:
    useless_variable = "I'm a useless variable! "
                                                                                                                #code starts here######################################
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:////database_prototype.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) 

class User(db.Model):
    __tablename__ = "accounts"
    account_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)  
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    account_date_of_creation = db.Column(db.DateTime, nullable=False)
    account_status = db.Column(db.String(32), nullable=False)

#with app.app_context():
#    db.create_all()

#db = SQLAlchemy(app)
migrate = Migrate(app, db)
    
@app.route("/home")
def home_page():
    users = User.query.all()  # Fetch all users from the database
    return f"Users: {users}"
    return render_template("home.html", show_buttons=True)
    
@app.route("/login", methods=["GET", "POST"])
def login_page():
    print(request.form)
    db = connect_to_db()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cursor = db.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE username = ? AND password = ? LIMIT 1)", (username, password,))  #program asks if a field with the given credentials exists
        exists = cursor.fetchone()[0]                                                                                   
        if exists:                                                                                                                  #if an account with the given credentials exists then the session_id is made equal to that accounts id
            cursor = db.execute("SELECT account_id FROM accounts WHERE username = ? AND password = ? ", (username, password,))
            details = cursor.fetchone()
            session[session_id] = int(details[0])
            print("The session id is:", session[session_id])
            print("You have logged in! ")
          
        else:
            cursor = db.execute("SELECT account_id FROM accounts WHERE username = ?", (username,))
            temp_name = cursor.fetchone()
            print("temp_name is:", temp_name)
            print("The login credentials that you have entered are incorrect. ")
            
    cursor = db.execute("SELECT account_id FROM accounts WHERE username = 'Tobias'")
    name = cursor.fetchone()
    print("The test name is:", name)
    return render_template("login.html")
        
@app.route("/signup")
def signup_page():
    return render_template("signup.html")
        
if __name__ == "__main__":
    app.run(debug = True)
