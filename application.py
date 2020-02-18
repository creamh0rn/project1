import os
import flask

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    output_text = "tester"
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if flask.request.method == "GET":
        return render_template("index.html")
    else:
        #run a query to see if they're in there
        #if not, send to sign up sheet
        #if yes, log them in?

        email_address = request.form.get("email_address")
        password = request.form.get("password")
        session['smang_it'] = "smash it and hit it"

        if db.execute("SELECT * FROM USERS WHERE EMAIL_ADDRESS = :email_address", {"email_address": email_address}).rowcount == 1:
            if db.execute("SELECT * FROM USERS WHERE EMAIL_ADDRESS = :email_address and PASSWORD = :password", {"email_address": email_address, "password": password}).rowcount == 1:
                session['logged_in'] = True

                return redirect(url_for('home'))
            else:
                return render_template("error.html", error_message= "incorrect password")
        else:
            return render_template("signup.html", email_address=email_address, password=password)


@app.route("/user_account", methods=["GET", "POST"])
def user_account():
    #method = post
    if flask.request.method == "POST":
        #collect variables
        email_address = request.form.get("email_address")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birthday = request.form.get("birthday")

        if db.execute("SELECT * FROM USERS WHERE EMAIL_ADDRESS = :email_address AND PASSWORD = :password",
                      {"email_address": email_address, "password": password}).rowcount == 0:
            db.execute("INSERT INTO USERS (EMAIL_ADDRESS, PASSWORD, FIRST_NAME, LAST_NAME, BIRTHDAY) VALUES (:EMAIL_ADDRESS, :PASSWORD, :FIRST_NAME, :LAST_NAME, :BIRTHDAY)", {"EMAIL_ADDRESS": email_address, "PASSWORD": password, "FIRST_NAME": first_name, "LAST_NAME": last_name, "BIRTHDAY": birthday})
            db.commit()

        else:
            return redirect(url_for('home'))

        message = session.get("smang_it")
        return render_template("error.html", error_message= message)
    #method = get
    else:
        if session.get("logged_in") == False:
            #not signed in
            return render_template("error.html", error_message = "not signed in")
        else:
            #home
            return render_template("error.html", error_message = "signed in")


@app.route("/home", methods=["POST", "GET"])
def home():

    return render_template("error.html", error_message= message)









@app.route("/sign_out", methods=["POST"])
def sign_out():
    session['logged_in'] = False
    return redirect(url_for('index'))
