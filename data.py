from flask import*
import sqlite3
import random
import datetime
import time
import os
from flask_toastr import Toastr
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt
engine = create_engine('sqlite:///iot_wqms_data.db')
db=scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

toastr = Toastr(app)

con = sqlite3.connect('iot_wqms_data.db')
# con = sqlite3.connect(':memory:') # when db locks
cursor = con.cursor()

def create_table():

        cursor.execute(
                """ CREATE TABLE IF NOT EXISTS iot_wqms_table( 
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        Time TIMESdTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        temperature REAL, 
                        turbidity REAL,
                        ph REAL) """)
                        
        print('...inside create db fxn') 

# if not included, creates only DB without any table    
create_table()

def create_user():

        cursor.execute(
                """ CREATE TABLE IF NOT EXISTS users( 
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        name text NOT NULL, 
                        email text NOT NULL,
                        ml_number text NOT NULL,
                        password text NOT NULL) """)
                        
        print('...inside create db fxn') 

# if not included, creates only DB without any table    
create_user()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")
'''
def insertUser(name, email, ml_number, password):
    flash("Database Connected!")
    con = sqlite3.connect("iot_wqms_data.db")
    cur = con.cursor()
    
    cur.execute("INSERT INTO users (name,email,ml_number,password) VALUES (?,?,?,?)", (name, email, ml_number,password))
    con.commit()
    flash("Thanks for registering!")
    con.close()
    flash("Thanks for registering!")
    return render_template('index.html')

    try:
        
        flash("Database connected")
        cur.execute("SELECT id FROM users WHERE ml_number =?",(ml_number))
        rows = cur.fetchall()
        if rows is not None:
            flash("Querry Perform")
        
            flash("Database no one!")
            flash("That Medical License Number is already existed")
            return render_template('register.html')
        else:
     


@app.route('/add_users')
def add_users():
    name = request.args.get('name')
    email = request.args.get('email')
    ml_number = request.args.get('ml_number')
    password = request.args.get('password')
    cpassword= request.args.get('cpassword')

    

    if (password==cpassword):
        insertUser(name ,email, ml_number, password)
        print(name)
        print(email)
        print(ml_number)
        print(password)
        print(cpassword)
        flash("User Details inserted!")
        return redirect("/", code=302)
    else:
        flash("password must match!") 
        return render_template('register.html')
'''

@app.route('/add_data')
def add_data():
    temperature = request.args.get('temperature')
    pulse = request.args.get('pulse')
    respiration = request.args.get('respiration')
    print(temperature)
    print(pulse)
    print(respiration)
    add_to_db(temperature,pulse,respiration)
    return redirect("localhost:5000/records.html", code=302)


def add_to_db(temperature, pulse, respiration):
    con = sqlite3.connect('iot_wqms_data.db')
    c = con.cursor()
    c.execute(""" INSERT INTO iot_wqms_table( temperature, turbidity, ph) 
                         VALUES (?, ?, ?) """,
                   (temperature,pulse, respiration))
    flash("data inserted SUCCESSFULLY", "success")
    con.commit()
    print("Data inserted SUCCESSFULLY")








    #register form
@app.route("/register",methods=["GET","POST"])
def registered():
    if request.method=="POST":
        name=request.form.get("name")
        email=request.form.get("email")
        ml_number =request.form.get("ml_number")
        password=request.form.get("password")
        confirm=request.form.get("confirm")
        secure_password=sha256_crypt.encrypt(str(password))

        print(name)

        usernamedata=db.execute("SELECT email FROM users WHERE email=:email",{"email":email}).fetchone()
        #usernamedata=str(usernamedata)
        if usernamedata==None:
            if password==confirm:
                db.execute("INSERT INTO users(name,email, ml_number, password) VALUES(:name,:email,:ml_number, :password)",
                    {"name":name,"email":email,"ml_number":ml_number, "password":secure_password})
                db.commit()
                flash("You are registered and can now login","success")
                return redirect(url_for('login'))
            else:
                flash("password does not match","danger")
                return render_template('register.html')
        else:
            flash("user already existed, please login or contact admin","danger")
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        email=request.form.get("email")
        password=request.form.get("password")
        usernamedata=db.execute("SELECT email FROM users WHERE email=:email",{"email":email}).fetchone()
        passworddata=db.execute("SELECT password FROM users WHERE email=:email",{"email":email}).fetchone()

        if usernamedata is None:
            flash("No User","danger")
            return render_template('register.html')
        else:
            for passwor_data in passworddata:
                if sha256_crypt.verify(password,passwor_data):
                    session["log"]=True
                    flash("You are now logged in!!","success")
                    return render_template("records.html")
                else:
                    flash("incorrect password","danger")
                    return render_template('index.html')
    
    return render_template('index.html')




if __name__ == '__main__':
    app.run()