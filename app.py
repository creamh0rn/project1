import os
import flask
import requests
import json

from flask import Flask, session, render_template, request, redirect, url_for, app
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
        return redirect(url_for("home"))

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

                return redirect(url_for("home"))
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

        session["user"] = db.execute("SELECT * FROM USERS WHERE EMAIL_ADDRESS = :EMAIL_ADDRESS and PASSWORD = :PASSWORD", {"EMAIL_ADDRESS":email_address, "PASSWORD": password}).fetchone()

        user = session.get["user"]


        return render_template("error.html", error_message = user[0])



@app.route("/home", methods=["POST", "GET"])
def home():
    if flask.request.method == "GET":
        return render_template("home.html")
    else:
        search_bar = "%" + str(request.form.get("search_bar")) + "%"
        if len(search_bar)==2:
            return render_template("home.html")
        else:
            results = db.execute("select * from books where isbn like :search_bar or lower(title) like lower(:search_bar) or lower(author) like lower(:search_bar)", {"search_bar":search_bar}).fetchall()
            return render_template("home.html", books = results)


@app.route("/book", methods=["POST", "GET"])
def book():
    if flask.request.method == "GET":
        return redirect(url_for("index"))
    else:
        isbn = request.form.get("book")
        book = db.execute("select * from books where isbn = :isbn", {"isbn":isbn}).fetchone()
        title = book[1]
        author = book[2]
        year = book[3]

        key = "6YiIpG7a9sWusuN44erRVQ"

        res = requests.get("https://www.goodreads.com/book/review_counts.json",
                           params={"key": key, "isbns": isbn})

        data = res.json()

        average_rating = data['books'][0]['average_rating']
        number_ratings = data['books'][0]['work_ratings_count']






        return render_template("book.html", number_ratings = number_ratings, book = book, average_rating=average_rating)








@app.route("/sign_out", methods=["POST"])
def sign_out():
    session['logged_in'] = False
    return redirect(url_for('index'))


