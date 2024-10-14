import sqlite3
import time
import datetime

session_id = 0

def login():                                                                                                                    #login() function is defined
    global session_id                                                                                                           #session_id is made global for so that it can be modified within the signup() function if the need arises
    cursor.execute("SELECT COUNT(*) FROM accounts")
    result = cursor.fetchone()
    result = int(result[0])
    if result == 0:
        print("No accounts currently exist on this system. ")
    username = input("Enter a username: ")                                                                                      #user is asked for their username 
    if username != "Tobias":
        username = username.lower()
    password = input("Enter a password: ")                                                                                      #user is asked for their password
    cursor.execute("SELECT account_status FROM accounts WHERE username = ? AND password = ?", (username, password,))
    result = cursor.fetchone()
    status = result[0]
    if status == "banned":
        print("Your account has been banned and you are unable to login. ")
        home()
    cursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE username = ? AND password = ? LIMIT 1)", (username, password,))  #program asks if a field with the given credentials exists
    exists = cursor.fetchone()[0]                                                                                   
    if exists:                                                                                                                  #if an account with the given credentials exists then the session_id is made equal to that accounts id
        cursor.execute("SELECT account_id FROM accounts WHERE username = ? AND password = ? ", (username, password,))
        details = cursor.fetchone()
        session_id = int(details[0])
        print("You have logged in! ")
        home()
    else:
        print("The login credentials that you have entered are incorrect. ")
        home()
        
class login:
    def __init__(self, username, password):
        self.username = username 
        self.password = password
        
    def login_verification(self, username, password):
        cursor.execute("SELECT account_status FROM accounts WHERE username = ? AND password = ?", (username, password,))
        status = cursor.fetchone()
        if status == "banned":
            #flash message 
    cursor.execute("SELECT EXISTS(SELECT 1 FROM accounts WHERE username = ? AND password = ? LIMIT 1)", (username, password,))  #program asks if a field with the given credentials exists
    exists = cursor.fetchone()[0]                                                                                   
    if exists:                                                                                                                  #if an account with the given credentials exists then the session_id is made equal to that accounts id
        cursor.execute("SELECT account_id FROM accounts WHERE username = ? AND password = ? ", (username, password,))
        details = cursor.fetchone()
        session_id = int(details[0])
        #flash
        time.sleep(3)
        #redirect to homepage
    else:
        #flash
        