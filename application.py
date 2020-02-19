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


@app.route("/", methods=["GET"])
def index():
    if session.get("logged_in") == False:
        return render_template("index.html", visible= "hidden")
    else:
        return redirect(url_for('home'))

@app.route("/sign_in", methods=["POST", "GET"])
def sign_in():
    if flask.request.method == "GET":
        return redirect(url_for('index'))
    else:
        email_address = request.form.get("email_address")
        password = request.form.get("password")

        if db.execute("SELECT * FROM USERS WHERE EMAIL_ADDRESS = :email_address",
                      {"email_address": email_address}).rowcount == 1:
            if db.execute("SELECT * FROM USERS WHERE EMAIL_ADDRESS = :email_address and PASSWORD = :password",
                          {"email_address": email_address, "password": password}).rowcount == 1:
                session['logged_in'] = True

                return redirect(url_for('home'))
            else:
                return render_template("index.html", error_message="Incorrect Password! Please try again", email_address = email_address, visible = "hidden")
        else:
            return render_template("signup.html", email_address=email_address, password=password, visible = "hidden")


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if flask.request.method == "GET":
        return redirect(url_for('index'))
    else:
        # collect variables
        email_address = request.form.get("email_address")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        birthday = request.form.get("birthday")

        db.execute(
            "INSERT INTO USERS (EMAIL_ADDRESS, PASSWORD, FIRST_NAME, LAST_NAME, BIRTHDAY) VALUES (:EMAIL_ADDRESS, :PASSWORD, :FIRST_NAME, :LAST_NAME, :BIRTHDAY)",
            {"EMAIL_ADDRESS": email_address, "PASSWORD": password, "FIRST_NAME": first_name, "LAST_NAME": last_name,
             "BIRTHDAY": birthday})
        db.commit()

        x = db.execute("SELECT USER_ID, EMAIL_ADDRESS, PASSWORD FROM USERS WHERE EMAIL_ADDRESS = :EMAIL_ADDRESS and PASSWORD = :PASSWORD", {"EMAIL_ADDRESS":email_address, "PASSWORD": password}).fetchone()


        return render_template("error.html", error_message = x[0])











@app.route("/home", methods=["POST", "GET"])
def home():

    return render_template("error.html", error_message= "main page")









@app.route("/sign_out", methods=["POST"])
def sign_out():
    session['logged_in'] = False
    return redirect(url_for('index'))
